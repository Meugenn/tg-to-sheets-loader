import gspread
from oauth2client.service_account import ServiceAccountCredentials
from subs import subjects

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('google_api_data.json', scope)

client = gspread.authorize(creds)


wks = client.open("Икт").sheet1

def update_homework(subject, text):
    coords = subjects[subject]
    wks.update_cell(coords[0], coords[1], text)

# print(wks.range('B17:C81'))

# def get_homeworks():