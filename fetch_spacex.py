import requests
from pathlib import Path
import logging
from load_in_web_to_dir import download_image_from_web


def fetch_spacex_launch(dir_name, num_launch=108) -> None:
    """Загрузка фотографий запуска SpaceX в указанную папку. По умолчанию пытается загрузить 108"""
    if 0 >= num_launch:
        logging.warning('Попытка получить фотографии SpaceX c нулевым или отрицательным номером')
        return
    url = 'https://api.spacexdata.com/v3/launches/next'
    response = requests.get(url)
    response.raise_for_status()
    next_launch_id = response.json()['flight_number']
    if num_launch >= next_launch_id:
        logging.warning('Попытка получить фотографии SpaceX c будущего старта')
        return
    url = 'https://api.spacexdata.com/v3/launches/'
    payload = {
        'flight_number': num_launch,
        'filter': 'links/flickr_images',
    }
    response = requests.get(url, payload)
    response.raise_for_status()
    links = response.json()

    for img_numb, link_img in enumerate(links[0]['links']['flickr_images'], start=1):
        filename = f'spacex{img_numb:02}.jpg'
        download_image_from_web(dir_name, link_img, filename)
        logging.info(f'save {img_numb} img')


def load_images_spacex(dir_name):
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    fetch_spacex_launch(dir_name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
    dir_name = 'images'
    load_images_spacex(dir_name)
