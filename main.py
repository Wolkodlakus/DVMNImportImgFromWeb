import requests
from pathlib import Path
import json
import os
from os.path import splitext
from urllib.parse import urlparse, unquote

import telegram as telegram
from dotenv import load_dotenv



def load_images_from_web(dir, url_img, name_img) -> None:
    response = requests.get(url_img)
    response.raise_for_status()
    with open(Path(dir, name_img), 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch() -> None:
    url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.get(url)
    print('Начинаем загрузку фотографий запуска spacex')
    if response.status_code == 404:  # and not response.ok:
        print('Страницы последнего запуска нет. Грузим с 108-го запуска')
        url = 'https://api.spacexdata.com/v3/launches/'
        payload = {
            'flight_number': 108,

            'filter': 'links/flickr_images',
        }
    else:
        payload = {
            'filter': 'links/flickr_images',
        }
    response = requests.get(url, payload)
    response.raise_for_status()

    links = json.loads(response.text)

    for img_numb, link_img in enumerate(links[0]['links']['flickr_images']):
        filename = f'spacex{(img_numb+1):02}.jpg'
        load_images_from_web(dir_name, url, filename)
        print(f'save {img_numb+1} img')


def give_file_extension(url_string):
    return (splitext(find_filename_in_url(url_string))[-1])


def find_filename_in_url(url_string):
    filepath = urlparse(unquote(url_string)).path
    _, filename = os.path.split(filepath)
    return filename


def load_APOD(num_photo):
    print('Начинаем загрузку фотографий APOD')
    url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': NASA_API_KEY,
        'count': num_photo,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    dir_name = 'images/images_APOD'
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    for img_numb, item in enumerate(response.json()):
        url_item = item['url']
        filename = f'APOD{(img_numb + 1):02}{give_file_extension(url_item)}'
        if len(give_file_extension(url_item)) > 0:
            load_images_from_web(dir_name, url_item, filename)
        else:
            print(f'Не адрес фотографии -{url_item}')


def load_EPIC():
    print('Начинаем загрузку фотографий EPIC')
    url = 'https://api.nasa.gov/EPIC/api/natural'
    params = {
        'api_key': NASA_API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    url_archive = 'https://api.nasa.gov/EPIC/archive/natural/'
    dir_name = 'images/images_EPIC'
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    for item in response.json():
        date_time_item = item['date']
        identifier = item['identifier']
        name_image = item['image']
        url_item = f'{url_archive}{identifier[:4]}/{identifier[4:6]}/{identifier[6:8]}/png/{name_image}.png'
        filename = f'{name_image}.png'
        url = f'{url_item}?api_key={NASA_API_KEY}'
        load_images_from_web(dir_name, url, filename)


if __name__ == '__main__':
    load_dotenv()
    NASA_API_KEY = os.getenv('NASA_API_KEY')
    print('=' * 80)
    print('start')
    dir_name = 'images'
    # os.makedirs(dir_name, exist_ok=True)
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    fetch_spacex_last_launch()
    load_APOD(30)
    load_EPIC()
    TOKEN_TG = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    bot = telegram.Bot(token=TOKEN_TG)
    print(bot.get_me())
    bot.send_message(chat_id=CHAT_ID, text='Привет! Это сообщение от бота, назначенного админом этого канала')

    print('finish')
