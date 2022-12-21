import pandas as pd
import json
import requests

from upload_to import upload_events_by_cells, upload_events_to_csv


# Отправка кода авторизации и получение токена
def get_token():
    with open('data_authorization.json', 'r') as f:
        userdata = json.load(f)
    user = userdata['user']
    data = userdata['data']
    url1 = 'https://' + user + '.amocrm.ru/oauth2/access_token'
    r1 = requests.post(url1, data)
    if r1.status_code == 400:
        raise Exception("Authorization code has expired. Update authorization code.")
    with open('token.json', 'w') as f:
        r1 = r1.json()
        json.dump(r1, f)


# Получение логов событий
def log_events():
    with open('token.json', 'r') as f1,\
            open('data_authorization.json', 'r') as f2:
        userdata = json.load(f2)
        token = json.load(f1)
    user = userdata['user']
    access_token = token['access_token']
    refresh_token = token['refresh_token']
    user_url = f'http://{user}.amocrm.ru/'
    try:
        header = {'Authorization': 'Bearer ' + access_token}
        r = requests.get(user_url + '/api/v4/events', headers=header)
    except Exception:
        header = {'Authorization': 'Bearer ' + refresh_token}
        r = requests.get(user_url + '/api/v4/events', headers=header)
    with open('events.json', 'w') as f:
        r1 = r.json()
        json.dump(r1, f)


# Парсинг логов событий, перевод их в json, а затем в cvs формат
def parse_events():
    with open('events.json', 'r') as f:
        logs = json.load(f)
    events = logs['_embedded']['events']
    event_json = json.dumps(events)
    df = pd.read_json(event_json)
    df.to_csv('log_events.csv', encoding='utf-8', index=False)


def main():
    # Получение токена
    get_token()
    # Получение логов событий
    log_events()
    # Парсинг логов событий
    parse_events()

    # Вставляем сюда полученный токен файл для Google Drive API
    token_file = 'g_token.json'
    # Загружаем файл в гугл таблицы (в виде csv файла)
    upload_events_to_csv(file='log_events.csv', sheet_name='logs1.csv', token_file=token_file)
    # Загружаем файл в ячейку гугл таблицы
    upload_events_by_cells(file='log_events.csv', sheet_name='logs2.csv', token_file=token_file)


if __name__ == '__main__':
    main()
