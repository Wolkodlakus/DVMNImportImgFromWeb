# Учебный проект "Загрузите в Telegram фотографии космоса".

Раз в сутки приложение скачивает свежие фотографии (по возможности) от SpaceX, 
потом случайные фотографии APOX NASA, затем фотографии EPIC NASA за последние сутки 
и постит через бота в указанный канал Telegram, после чего удаляет файлы из локальной папки. 
___________________
## Требования
Нужен Python от версии 3.8.
Для работы с API NASA нужно получить ключ (https://api.nasa.gov/). 
Для работы с Telegram нужно получить токен бота и id канала.

## Установка / Getting Started 
- Скачайте код.
- Установите зависимости командой `pip install -r requirements.txt`

___________________
## Переменные окружения

Определите переменные окружения в файле `.env` в формате: `ПЕРЕМЕННАЯ=значение`:
- `NASA_API_KEY` — Ключ API, можно получить на сайте NASA https://api.nasa.gov/
- `TELEGRAM_TOKEN` - токен бота Telegram
- `CHAT_ID` - ID канала, где бот назначен админом
- `DELAY_BETWEEN_LAUNCHES` - задержка между запусками приложения, по умолчанию - 86400 секунд - сутки

___________________
## Использование
Проект состоит из 4 скриптов. 
### public_img2telegram.py
Основной скрипт. 

Здесь работает бесконечный цикл с задержкой, определяемой `DELAY_BETWEEN_LAUNCHES`.
В цикле происходит обращение к двум другим скриптам, которые скачивают свежие,
по возможности, фотографии в указанную папку (по умолчанию `images`). 
После вызывается функция постинга, которая с указанной задержкой 
(по умолчанию - сутки) кидает все картинки в указанный канал Telegram. 

После этого вызывается функция удаления папки с изображениями.


### fetch_spacex.py
Скрипт загрузки изображений запуска SpaceX. 
Если не указан точный номер, то загружается последний доступный на сегодня - 108 запуск. 
Основная функция - `load_images_spacex`, в которую передаётся папка, куда не обходимо сохранять.


### fetch_nasa.py
Скрипт загрузки изображений NASA с помощью API ключа. 
Здесь 2 функции - `load_apod` (загрузка случайного указанного количества фотографий APOD, по умолчанию 25), 
вторая - `load_epic` (загрузка фотографий EPIC за последние сутки).


## load_from_web_to_dir.py
Скрипт объединяет несколько функций для загрузки фото из интернета и сохранения их в локальную папку.

## Особенности.
Из-за учебного характера проекта, не все возможные ситуации отрабатываются. 
Нет перехвата исключений. Логгирование переключено на уровень INFO:
```
logging.basicConfig(level = logging.INFO)
```


