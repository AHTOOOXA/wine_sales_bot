import psycopg2
from psycopg2 import Error, sql
from configparser import ConfigParser
import logging
from datetime import date
from typing import List


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    _FILE_NAME = 'database.ini'
    _SECTION = 'postgresql'

    def _get_config(self):
        parser = ConfigParser()
        parser.read(self._FILE_NAME)
        # get section, default to postgresql
        config = {}
        if parser.has_section(self._SECTION):
            params = parser.items(self._SECTION)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self._SECTION, self._FILE_NAME))
        return config

    def __init__(self):
        self.conn = None  # type: psycopg2.connection
        self.cur = None  # type: psycopg2.cursor
        self.config = self._get_config()
        self._create_connection()
        self._create_wine_table()

    def __del__(self):
        self._close_connection()

    def _create_connection(self):
        try:
            # raise exception is config not set
            self.conn = psycopg2.connect(**self.config)
            self.cur = self.conn.cursor()
            print("DB INFO")
            print(self.conn.get_dsn_parameters(), "\n")
        except (Exception, Error) as error:
            print("ERROR PostgreSQL", error)
        finally:
            if self.conn:
                print("DB CONNECTION SUCCEEDED\n")

    def _close_connection(self):
        if self.conn:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            print("DB CONNECTION CLOSED")

    def _create_wine_table(self):
        field_names = {'name': 'VARCHAR(255)',  # getting this from scrapy spiders
                       'price_new': 'FLOAT',
                       'price_old': 'FLOAT',
                       'updated': 'VARCHAR(255)',
                       'shop': 'VARCHAR(255)',
                       'url': 'VARCHAR(255)',
                       'rating': 'FLOAT',  # getting these from vivino_scraper in rate_new_vines
                       'rating_count': 'INT',
                       'vivino_url': 'VARCHAR(255)',
                       'img_url': 'VARCHAR(255)',
                       'post_id': 'VARCHAR(255)',
                       }
        query = """CREATE TABLE IF NOT EXISTS {table} ({fields})""".format(
            table='wines',
            fields=', '.join(
                [' '.join([item[0], item[1]]) for item in field_names.items()]
            ))
        self.cur.execute(query)
        # dropping and adding constraint to avoid relation "uc" already exists if table has existed before
        query = """ALTER TABLE wines DROP CONSTRAINT IF EXISTS uc"""
        self.cur.execute(query)
        query = """ALTER TABLE wines ADD CONSTRAINT uc UNIQUE (name)"""
        self.cur.execute(query)
        self.conn.commit()

    # def delete_wine_table(self):
    #     query = """DROP TABLE {table}""".format(
    #         table='wines'
    #     )
    #     logging.info(query)
    #     self.cur.execute(query)
    #     self.conn.commit()

    def insert_wine(self, item):
        try:
            field_names = ['name',
                           'price_new',
                           'price_old',
                           'updated',
                           'shop',
                           'url',
                           'rating',
                           ]
            fields_to_update = ['price_new',
                                'price_old',
                                'url',
                                'updated',
                                ]
            query = sql.SQL("""INSERT INTO wines ({fields}) VALUES ({values})
            ON CONFLICT ON CONSTRAINT uc DO UPDATE SET {updates}""").format(
                fields=sql.SQL(', ').join(map(sql.Identifier, field_names)),
                values=sql.SQL(', ').join(map(sql.Literal, [item[f] for f in field_names])),
                updates=sql.SQL(', ').join(
                    sql.Composed([sql.Identifier(f), sql.SQL(" = "), sql.Literal(item[f])]) for f in fields_to_update
                ),
            )
            self.cur.execute(query)
            logging.info(f"Successfully inserted wine: {item['name']}")
        except Exception as e:
            logging.error(f"Error in insert_wine(): {e}")
        finally:
            self.conn.commit()

    def update_wine_vivino(self, item):
        try:
            field_names = ['rating',
                           'rating_count',
                           'vivino_url',
                           'img_url',
                           ]
            query = sql.SQL("""UPDATE wines SET {updates} WHERE name={name}""").format(
                name=sql.Literal(item['name']),
                updates=sql.SQL(', ').join(
                    sql.Composed([sql.Identifier(f), sql.SQL(" = "), sql.Literal(item[f])]) for f in field_names
                )
            )
            self.cur.execute(query)
            logging.info(f"Successfully updated vivino rating for wine: {item['name']}")
        except Exception as e:
            logging.error(f"Error in update_wine_vivino(): {e}")
        finally:
            self.conn.commit()

    def get_wines_to_rate(self) -> List[str]:
        query = sql.SQL("""SELECT name FROM wines WHERE rating = -1""")
        self.cur.execute(query)
        wine_names = [tup[0] for tup in self.cur.fetchall()]
        return wine_names

    # add true tracing if wine was really posted in tg (currently it sets posted to true even if it was only fetched
    # to post)
    def get_wines_to_post(self):
        query = sql.SQL("""SELECT * FROM wines WHERE rating >= 4.0 AND post_id IS NULL""")
        self.cur.execute(query)
        good_wines = self.cur.fetchall()
        query = sql.SQL("""UPDATE wines SET post_id = 'posted' WHERE rating >= 4.0 AND post_id IS NULL""")
        self.cur.execute(query)
        self.conn.commit()
        return good_wines

    def count_new_wines(self) -> int:
        query = sql.SQL("""SELECT name FROM wines WHERE rating = -1""")
        self.cur.execute(query)
        wines = self.cur.fetchall()
        counter = 0
        for wine in wines:
            print(wine)
            counter += 1
        return counter

    def clean_up(self):
        query = sql.SQL("""SELECT COUNT(name) FROM wines WHERE updated != {date}""").format(
            date=sql.Literal(date.today().strftime("%Y-%m-%d"))
        )
        self.cur.execute(query)
        outdated_wines_count = self.cur.fetchall()
        logging.info(f"Outdated wines count: {outdated_wines_count}")

        query = sql.SQL("""DELETE FROM wines WHERE updated != {date}""").format(
            date=sql.Literal(date.today().strftime("%Y-%m-%d"))
        )
        self.cur.execute(query)
        logging.info(f"DELETED {outdated_wines_count} outdated wines")
        self.conn.commit()
