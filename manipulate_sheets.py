import Google_API_methods


def duplicate_spreadsheet(spreadsheet,  destination_Drive_folder_ID):
    """Duplicates the given spreadsheet if it doesn't already exist in the destination folder."""
    original_spreadsheet = Google_API_methods.sheets_service.spreadsheets().get(spreadsheetId=spreadsheet['id'])\
        .execute()
    if already_existing(original_spreadsheet, destination_Drive_folder_ID):
        return False
    else:
        duplicated_file = Google_API_methods.drive_service.files().copy(fileId=spreadsheet['id'],
                                                                        body=original_spreadsheet).execute()
        return duplicated_file


def already_existing(spreadsheet, destination_Drive_folder_ID):
    """Checks for existing spreadsheet in the destination folder; this is to prevent duplicates from being made
    of existing files."""
    is_existing = False

    if (len(Google_API_methods.drive_service.files().list(q=destination_Drive_folder_ID + " in parents and name='" +
                                                          Google_API_methods.drive_service.files()
                                                          .get(fileId=spreadsheet['spreadsheetId'],
                                                               fields='name').execute()['name'] +
                                                          "' and trashed=False").execute()['files'])) > 0:
        is_existing = True

    return is_existing


def move_to_new_folder(file, destination_Drive_folder_ID):
    """Moves duplicated spreadsheet to the destination folder folder."""
    file_parents = Google_API_methods.drive_service.files().get(fileId=file['id'], fields='parents').execute()

    previous_parents = ", ".join(file_parents.get('parents'))
    Google_API_methods.drive_service.files().update(fileId=file['id'],
                                                    addParents=destination_Drive_folder_ID.strip("'"),
                                                    removeParents=previous_parents, fields='id, parents').execute()


def remove_copyof_prefix(file):
    """Removes the 'Copy of' prefix in Google Drive from a copied file."""
    if file['name'].startswith('Copy of '):
        Google_API_methods.drive_service.files().update(fileId=file['id'],
                                                        body={'name': file['name'][len('Copy of '):]}).execute()


def delete_sheet_in_spreadsheet(file, sheet_title):
    """Within the spreadsheet passed in, deletes the sheet with the matching name if there is one."""
    spreadsheet = Google_API_methods.sheets_service.spreadsheets().get(spreadsheetId=file['id']).execute()

    for sheet in spreadsheet['sheets']:
        if sheet['properties']['title'] == sheet_title:
            batch_update_requests = {
                'requests': [
                    {
                        "deleteSheet": {
                            "sheetId": sheet['properties']['sheetId']
                        }
                    }
                ]
            }
            Google_API_methods.sheets_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet['spreadsheetId'],
                                                                         body=batch_update_requests).execute()


def header_title_check(file, headers_list):
    """Checks that each column in the given spreadsheet matches with the proper title."""
    spreadsheet = Google_API_methods.sheets_service.spreadsheets().get(spreadsheetId=file['id']).execute()
    get_spreadsheet_header = Google_API_methods.sheets_service.spreadsheets().values().\
        get(spreadsheetId=spreadsheet['spreadsheetId'], range="A1:AH1").execute()['values']

    for template_value in range(len(headers_list)):
        if headers_list[template_value] != get_spreadsheet_header[0][template_value]:
            print("Differing header found in " + spreadsheet['properties']['title'] + "!\n"
                  + headers_list[template_value] + " was found in the expected place of " +
                  str(get_spreadsheet_header[0][template_value]) + " from your headers list.")






