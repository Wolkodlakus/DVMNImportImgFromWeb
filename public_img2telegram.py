from fetch_spacex import load_images_spacex
from fetch_nasa import load_images_nasa
from telegram import Bot
from dotenv import load_dotenv
import os
import shutil
import time
import logging


def del_images(dir_name):
    logging.info('Удаляем папку с картинками')
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), dir_name)
    shutil.rmtree(path)


def post_img_to_tg_channel(bot, chat_id, dir_name):
    """Постинг фотографий ботом из папки/папок в канал"""
    for root, dirs, files in os.walk(dir_name):
        files = [os.path.join(root, filename) for filename in files]
        for file in files:
            logging.info(f'Постим {file}')
            with open(file, 'rb') as img_file:
                photo = img_file.read()
            bot.send_photo(chat_id=chat_id, photo=photo)
            time.sleep(10)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.info('Запуск скрипта.')
    load_dotenv()
    nasa_api_key = os.getenv('NASA_API_KEY')
    token_tg = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    delay_between_launches = int(os.getenv('DELAY_BETWEEN_LAUNCHES'))
    dir_name = 'images'
    logging.debug(f'Папка для размещения картинок {dir_name}')
    while True:
        logging.info('Запуск цикла загрузки и постинга картинок.')
        logging.info('Начинаем скачивать с SpaceX.')
        load_images_spacex(dir_name)
        logging.info('Начинаем скачивать с NASA.')
        load_images_nasa(dir_name, nasa_api_key)

        bot = Bot(token=token_tg)
        logging.info('Запускаем постинг с бота.')
        post_img_to_tg_channel(bot, chat_id, dir_name)

        del_images(dir_name)
        logging.info('Ждём запуска нового цикла.')
        time.sleep(delay_between_launches)
