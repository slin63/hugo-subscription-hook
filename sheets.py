import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_subscribers():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("chronic pizza subscribe (Responses)").sheet1
    subscribers = sheet.col_values(2)[1:]  # [1:] so that we can omit the header

    return list(set(subscribers)), sheet


# Takes in a list of emails and removes them from the spreadsheet
def remove_subscribers(subscribers, sheet):
    to_update = []
    for s in subscribers:
        cells = sheet.findall(s)
        for c in cells:
            c.value = ""
            to_update.append(c)

    if to_update:
        sheet.update_cells(to_update)
