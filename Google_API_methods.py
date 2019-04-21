import pickle
import os.path
from googleapiclient.discovery import build


def get_credentials():
    """Returns existing Google credentials, created from Google's quickstart.py module."""
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            return creds
    else:
        print("No token detected; this program expects an already-existed token created through Google's API system. "
              "A token can be created by following the instructions at "
              "https://developers.google.com/drive/api/v3/quickstart/python, and changing the 'SCOPES' variable to "
              "the following: \n"
              "SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']"
              "Additionally, replace the line 'credentials.json' with your own credentials through Google's API System."
              " As this program requires moving, copying, and editing files in your Google Drive and Google Sheets, "
              "this level of permission is necessary.")


def get_sheets(folder_id):
    """Returns list of spreadsheets given the query parameters and folder id."""
    results_list = drive_service.files().list(q=folder_id + " in parents and " + "trashed=False",
                                              pageSize=999).execute()
    spreadsheets_list = results_list.get("files", [])
    return spreadsheets_list


drive_service = build('drive', 'v3', credentials=get_credentials())
sheets_service = build('sheets', 'v4', credentials=get_credentials())









