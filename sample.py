import manipulate_sheets
import CSV_functions
import socket
import Google_API_methods
import time
from googleapiclient import errors as Google_API_errors


origin_Drive_folder_ID = "Enter your origin folder ID here, surrounded by double and single quotes (i.e. "'12345'")"
destination_Drive_folder_ID = "Enter your destination folder ID here, surrounded by double and single quotes " \
                              "(i.e. "'12345'")"
spreadsheets = Google_API_methods.get_sheets(origin_Drive_folder_ID)
sheet_title_to_delete = "Enter the title of any sheets you'd want deleted by the delete_sheet_in_spreadsheet function" \
                        "here."
header_values = ['header 1', 'header 2', 'header 3']

def sample_function():
    """An example function that copies documents from the origin folder to the destination folder. It also deletes
    any sheets within the spreadsheets matching the title defined in sheet_title_to_delete, and checks for any
    spreadsheets with header values that don't match those listed in header_values. Then, the program
    downloads CSVs of the copied files, and combines them into a new, master CSV file."""
    try:
        for spreadsheet in spreadsheets:
            duplicated_file = manipulate_sheets.duplicate_spreadsheet(spreadsheet, destination_Drive_folder_ID)
            if not duplicated_file:
                pass
            else:
                manipulate_sheets.move_to_new_folder(duplicated_file, destination_Drive_folder_ID)
                manipulate_sheets.remove_copyof_prefix(duplicated_file)
                manipulate_sheets.delete_sheet_in_spreadsheet(duplicated_file, sheet_title_to_delete)
                manipulate_sheets.header_title_check(duplicated_file, header_values)

        folder_files = Google_API_methods.get_sheets(destination_Drive_folder_ID)
        for item in folder_files:
            CSV_functions.download_CSV(item)
        CSV_functions.create_master_CSV()
    except socket.timeout or Google_API_errors.HttpError:
        time.sleep(30)
        sample_function()



