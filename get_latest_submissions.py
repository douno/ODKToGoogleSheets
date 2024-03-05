import requests, json

from googleapiclient.discovery import build
from google.oauth2 import service_account

def write_to_doc(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

def read_json_file(filename):
    f = open(filename,)
    return json.load(f)

API_URL = 'https://westintelligence.com/v1/projects/2/forms/ANC_Visit.svc/Submissions'

r = requests.get(API_URL, auth=('YOUR_USERNAME', 'YOUR_PASSWORD'))
if r.status_code == 200:
    data = r.json()['value']
    write_to_doc('./data.json', data)

data = read_json_file('./data.json')

messages = []

for d in data:
    today = d['today']
    start_time = d['start_time']
    end_time = d['end_time']
    device_id = d['device_id']
    subscriber_id = d['subscriber_id']
    sim_serial = d['sim_serial']
    phone_number = d['phone_number']
    woman_name = d['woman_name']
    woman_id = d['woman_id']

    message = [
        today,
        start_time,
        end_time,
        device_id,
        subscriber_id,
        sim_serial,
        phone_number,
        woman_name,
        woman_id
    ]

    messages.append(message)


# Google Sheet API:
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1ndeivNNKtVZFZmN7cYVvNeRKgYl0ajb4tZLeYLp9br0'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Sheet1!A:A",
                                valueInputOption="USER_ENTERED",
                                body={"values":messages})
response = request.execute()
