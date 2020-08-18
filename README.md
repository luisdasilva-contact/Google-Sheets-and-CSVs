# Google Sheets and CSV Modules
A repository for Python modules to manipulate Google Sheets via Google Drive, and CSVs downloaded from Sheets. Note that functions that expect a file take a Google Drive file, while those expecting a spreadsheet take a Google Sheets file.

### Manipulate Sheets
manipulate.sheets.py contains functions to perform the following:
* Duplicate spreadsheets
* Check if a folder contains any spreadsheets
* Move a spreadsheet to a new folder
* Remove the 'Copy of' prefix assigned to duplicated spreadsheets
* Delete specificly-titled sheets within spreadsheets
* Check if a spreadsheet matches a user-defined header.

### CSV Functions
manipulate.sheets.py contains functions to perform the following:
* Download a CSV of a Google Sheets file. 
* Create a master CSV from all the CSVs in the directory. 

### Google API Methods
Google_API_methods.py contains the necessary service objects for communicating with the Google Drive and Sheets APIs. NOTE: This module assumes the user has an already-existing pickle token containing authorized credentials for the following scopes:
* https://www.googleapis.com/auth/drive
* https://www.googleapis.com/auth/spreadsheets

If you do not have such credentials, follow the instructions at one of Google's Python quickstart.py pages, such as the [Python Quickstart for Sheets](https://developers.google.com/sheets/api/quickstart/python). Remember to change the scopes listed in the quickstart.py file to the above!

### Sample
Sample.py contains a sample function utilizing each of the functions described above. 
