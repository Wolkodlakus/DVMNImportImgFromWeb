import os
from os.path import splitext
from pathlib import Path
import requests
from urllib.parse import urlparse, unquote


def download_image_from_web(dir, url_img, name_img, params=''):
    response = requests.get(url_img, params=params)
    response.raise_for_status()
    with open(Path(dir, name_img), 'wb') as file:
        file.write(response.content)


def find_filename_in_url(url_string):
    filepath = urlparse(unquote(url_string)).path
    _, filename = os.path.split(filepath)
    return filename


def give_file_extension(url_string):
    return splitext(find_filename_in_url(url_string))[-1]


if __name__ == '__main__':
    pass
