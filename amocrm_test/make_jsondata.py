import json


# Создание json файла с данными интеграции пользователя amo crm
def make_data_json():
    with open('data_authorization.json', 'w') as f:
        user = 'XXXX'
        data = {
            "client_id": "XXXX",
            "client_secret": "XXXX",
            "grant_type": "authorization_code",
            "code": "XXXX",
            "redirect_uri": "http://" + user + ".amocrm.ru/api/v4/events"
        }
        data_dict = {'user': user, 'data': data}
        json.dump(data_dict, f)


if __name__ == '__main__':
    make_data_json()
