from googleapiclient import discovery
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools
from argparse import ArgumentParser
import os

from import_feed import search_active_users

CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
APPLICATION_NAME = "my project"

range_ = "Fb_data_sheet!A1"


def writeToFile(service, data, spreadsheet_id):
    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, body={'values': data},
                                                     valueInputOption='RAW')
    response = request.execute()
    print(response)


def get_credentials(flags):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.esperanca.fb.data.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
    return credentials


def get_fb_data_for_sheets(fb_data):
    list_of_lists = []
    for key, value in fb_data.items():
        list_of_lists.append([str(key), value])
    return list_of_lists


def main():
    parser = ArgumentParser(parents=[tools.argparser])
    parser.add_argument('sheet_id', type=str)
    parser.add_argument('since', type=str)
    parser.add_argument('until', type=str)
    args = parser.parse_args()
    credentials = get_credentials(args)
    service = discovery.build('sheets', 'v4', credentials=credentials)
    data_in_dictionary_format = search_active_users(args.since, args.until)
    data_in_list_of_lists_format = get_fb_data_for_sheets(data_in_dictionary_format)

    writeToFile(service, data_in_list_of_lists_format, args.sheet_id)


if __name__ == "__main__":
    main()
