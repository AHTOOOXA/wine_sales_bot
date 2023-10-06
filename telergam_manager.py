import time
import requests
import os
import logging

TOKEN = os.environ['TOKEN']
CHANNEL = os.environ['CHANNEL']


class Telegram429(Exception):
    """raised when response code is 429"""
    pass


def post(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHANNEL, 'text': text, 'parse_mode': 'HTML'}
    try:
        response = requests.post(url=url, json=data)
    except Exception as e:
        logging.error(e)


def post_wine(wine) -> bool:
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    logging.info(f"Trying to post wine {wine[0]}")
    text = f"""<b>{wine[0]}</b>\n\n{wine[1]} ₽   <s>{wine[2]} ₽</s>\nРейтинг на Vivino: {wine[6]} <i>(число оценок: {wine[7]})</i>\n\n<a href="{wine[5]}">Страница в магазине</a>\n<a href="{wine[8]}">Страница на Vivino</a>\n\n{wine[4]}"""
    data = {'chat_id': CHANNEL, 'photo': wine[9], 'caption': text, 'parse_mode': 'HTML'}
    while True:
        try:
            response = requests.post(url, json=data)
            if response.status_code == 429:
                raise Telegram429
        except Telegram429:
            logging.error('Telegram429 error, sleeping for 60 sec and trying again')
            time.sleep(60)
            continue
        except Exception as e:
            logging.error(e)
            return False
        else:
            logging.info(f"Successfully posted wine {wine[0]}")
            return True
