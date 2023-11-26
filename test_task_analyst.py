import json
import openpyxl
import requests
from requests.auth import HTTPBasicAuth


def api_to_json(url, user, password):
    '''Функция для получения данных по API с базовой системой аутентицикации.
    Принимает url, user и password. '''
    responce = requests.get(url, auth=HTTPBasicAuth(user, password))
    status = responce.status_code
    if status == 200:
        data = responce.json()
        with open('sales_data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
        print(f'Данные получены, статус {status}. Сохранены в файле data.json')
    else:
        print(f'Не удалось получить данные, статус ответа сервера {responce.status_code}')


def json_to_excel(column_list, data):
    ''' Функция для создания таблицы Excel из json файла.
    Принимает список необходимых полей и словарь, прочитанный из json файла.'''
    # открываем книгу Excel
    book = openpyxl.Workbook()
    sheet = book.active

    # создаем список алфавита для заполнения столбцов
    alphabet = [chr(i).upper() for i in range(97, 123)]

    # Заполняем столбцы таблицы значениями из списка column_list
    i = 0
    for column in column_list:
        sheet[f'{alphabet[i]}1'] = column
        i += 1
    # Заполняем таблицу значениями из словаря data
    row = 2
    i = 0
    for product in data['data']:
        for column in column_list:
            sheet[row][i].value = product[column]
            i += 1
        row += 1
        i = 0
    # закрываем книгу Excel
    book.save('my_book_data.xlsx')
    book.close()
    print('Заполнена и сохранена таблица в файле sales_data.xlsx')


url = 'http://134.17.5.8:5000/get_data'
user = 'user2'
password = 'password2'

# Получаем данные по API, сохраняем json.
api_to_json(url, user, password)

# Переносим данные из json в Excel
with open('sales_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

column_list = ['name', 'brand', 'category', 'rating', 'seller', 'country', 'url', 'basic_price', 'basic_sale',
               'final_price', 'final_price_median', 'final_price_min', 'final_price_max', 'date']

json_to_excel(column_list, data)
