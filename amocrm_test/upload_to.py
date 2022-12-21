import gspread
from oauth2client.service_account import ServiceAccountCredentials


def connect(sheet_name, token):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(token, scope)
    client = gspread.authorize(credentials)
    try:
        sheet = client.open(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = client.create(sheet_name)
    sheet.share('sansmikh@gmail.com', perm_type='user', role='writer')
    return client, sheet


def upload_events_to_csv(sheet_name, file, token_file):
    client, sheet = connect(sheet_name, token_file)
    with open(file, 'r') as f:
        content = f.read()
        client.import_csv(file_id=sheet.id, data=content)


def upload_events_by_cells(sheet_name, file, token_file):
    client, sheet = connect(sheet_name, token_file)
    with open(file, 'r') as f:
        content = f.read()
    worksheet = sheet.get_worksheet(0)
    num = 1
    try:
        while True:
            val = worksheet.acell(f'A{num}').value
            if not val:
                worksheet.update(f'A{num}', content)
                break
            else:
                num += 1
                continue
    except Exception as e:
        print(f'Возникла ошибка: {e}')


if __name__ == '__main__':
    upload_events_by_cells('log_events.csv')
