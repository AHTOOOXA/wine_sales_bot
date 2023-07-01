import json

from bs4 import BeautifulSoup
import requests
import logging
import time


def get_vivino_rating_2(wine_name: str) -> tuple:
    while True:
        try:
            # getting particular wine page url
            url = f"https://www.vivino.com/search/wines?q={wine_name}"
            # move headers out
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
            }
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")
            wine_url_id = soup.find('div', class_='wine-card__image-wrapper').find('a')['href']
            wine_url = f"https://www.vivino.com{wine_url_id}"
            # collecting data for wine
            page = requests.get(wine_url, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")
            data = json.loads(soup.find('script', type='application/ld+json').text)
            rating = data['aggregateRating']['ratingValue']
            rating_count = data['aggregateRating']['ratingCount']
            img_url = f"""http:{soup.find('img', class_='image').attrs['src']}"""
            vivino_url = data['url']
            return rating, rating_count, img_url, vivino_url
        except BaseException as e:
            if page.status_code != 200:
                logging.error(f"VIVINO UNAVAILABLE status_code {page.status_code}\n SLEEP FOR 300 SEC")
                time.sleep(300)
            else:
                logging.error(f"ERROR in get_viviono_rating(): {e}.\nfor wine {wine_name}")
                return -2, -2, 'error', 'error'
