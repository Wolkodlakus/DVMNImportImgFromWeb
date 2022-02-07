import requests
from pathlib import Path
import os
from os.path import splitext
from urllib.parse import urlparse, unquote
import logging


def download_image_from_web(dir, url_img, name_img, params='') -> None:
    response = requests.get(url_img, params=params)
    response.raise_for_status()
    with open(Path(dir, name_img), 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(dir_name) -> None:
    """Загрузка фотографий последнего запуска SpaceX в указанную папку"""
    url = 'https://api.spacexdata.com/v3/launches/latest'
    response = requests.get(url)
    if not response.ok:
        # response.status_code == 404 ok включает не только 404, а причина может быть другой
        logging.warning('Страницы последнего запуска нет. Грузим с 108-го запуска')
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
    links = response.json()

    for img_numb, link_img in enumerate(links[0]['links']['flickr_images'], start=1):
        filename = f'spacex{img_numb:02}.jpg'
        download_image_from_web(dir_name, link_img, filename)
        logging.info(f'save {img_numb} img')


def give_file_extension(url_string):
    return splitext(find_filename_in_url(url_string))[-1]


def find_filename_in_url(url_string):
    filepath = urlparse(unquote(url_string)).path
    _, filename = os.path.split(filepath)
    return filename


def create_dir(dir_name):
    Path(dir_name).mkdir(parents=True, exist_ok=True)


def load_images_spacex(dir_name):
    create_dir(dir_name)
    fetch_spacex_last_launch(dir_name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
    dir_name = 'images'
    load_images_spacex(dir_name)
