import time
import requests
import os
import logging

TOKEN = os.environ['TOKEN']
CHANNEL = os.environ['CHANNEL']


class Telegram429(Exception):
    """raised when response code is 429"""
    pass


def post_to_telegram(wine) -> bool:
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    logging.info(f"Trying to post wine {wine[0]}")
    text = f"""<b>{wine[0]}</b>\n\n{wine[1]} ₽   <s>{wine[2]} ₽</s>\nРейтинг на Vivino: {wine[7]} <i>(число оценок: {wine[8]})</i>\n\nКупить: {wine[4]}\nСтраница на Vivino: {wine[10]}\n\n{wine[3]}"""
    data = {'chat_id': CHANNEL, 'photo': wine[9], 'caption': text, 'parse_mode': 'HTML'}
    while True:
        try:
            response = requests.post(url, json=data)
            if not response.ok:
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
