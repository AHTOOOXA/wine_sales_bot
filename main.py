import schedule
import telergam_manager
from db_manager import Database
import parsing
import logging

db = Database()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    db.create_wine_table()
    daily_routine()
    schedule.every(24).hours.do(daily_routine)
    while True:
        schedule.run_pending()


def daily_routine() -> None:
    logging.info('Started daily routine!!!')
    parsing.scrap()
    db.rate_new_wines()
    db.clean_up()
    good_wines = db.get_wines_to_post()
    for wine in good_wines:
        telergam_manager.post_to_telegram(wine)


if __name__ == '__main__':
    main()
