import logging
from datetime import datetime
import requests
from pathlib import Path
import os
from dotenv import load_dotenv
from load_in_web_to_dir import download_image_from_web, give_file_extension


def load_apod(dir_name, nasa_key, num_photo=25):
    """Загрузка некоторое количество фотографий APOD в указанную папку"""
    logging.info('Начинаем загрузку фотографий APOD')
    url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': nasa_key,
        'count': num_photo,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    for img_numb, item in enumerate(response.json(), start=1):
        url_item = item['url']
        filename = f'APOD{img_numb:02}{give_file_extension(url_item)}'
        logging.info(f'save {img_numb} img')
        if give_file_extension(url_item):
            download_image_from_web(dir_name, url_item, filename)
        else:
            logging.warning(f'По данному адресу не фотографии -{url_item}')


def load_epic(dir_name, nasa_key):
    """Загрузка последних фотографий EPIC в указанную папку"""
    logging.info('Начинаем загрузку фотографий EPIC')
    url = 'https://api.nasa.gov/EPIC/api/natural'
    params = {
        'api_key': nasa_key,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    url_archive = 'https://api.nasa.gov/EPIC/archive/natural/'
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    for img_numb, item in enumerate(response.json(), start=1):
        date_time_item = datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S')
        name_image = item['image']
        url_item = f'{url_archive}' \
                   f'{date_time_item.year:04}/' \
                   f'{date_time_item.month:02}/' \
                   f'{date_time_item.day:02}/' \
                   f'png/{name_image}.png'
        filename = f'{name_image}.png'
        params = {
            'api_key': nasa_key,
        }
        logging.info(f'save {img_numb} img')
        download_image_from_web(dir_name, url_item, filename, params)


def load_images_nasa(dir_name, nasa_key):
    load_apod(dir_name, nasa_key, 5)
    load_epic(dir_name, nasa_key)


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
    nasa_api_key = os.getenv('NASA_API_KEY')
    dir_name = 'images'
    load_images_nasa(dir_name, nasa_api_key)
