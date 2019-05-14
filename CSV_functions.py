import io
from googleapiclient.http import MediaIoBaseDownload
import glob
from Google_API_methods import sheets_service, drive_service
import csv


def download_CSV(spreadsheet):
    """Download the given spreadsheet as a .CSV file."""
    sheet_to_drive = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet['id']).execute()
    request = drive_service.files().export_media(fileId=spreadsheet['id'], mimeType='text/csv')
    CSV_file = io.FileIO(sheet_to_drive['properties']['title'] + ".csv", 'wb')
    downloader = MediaIoBaseDownload(CSV_file, request)
    done = False
    
    while done is False:
        status, done = downloader.next_chunk()


def create_master_CSV():
    """From any CSVs in the directory, create one master CSV containing each document."""
    CSV_files = glob.glob('./*.csv')

    for CSV in CSV_files:
        with open(CSV, 'r') as file:
            reader = file.read()

        with open("master_sheet.csv", "a") as master_file:
            master_file.write(reader)
            master_file.write('\n')
            master_file.close()
