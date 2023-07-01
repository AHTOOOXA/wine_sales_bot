import psycopg2
import logging
from db_manager import Database


class SavingToPostgresPipeline(object):
    def __init__(self):
        self.database = Database()

    def process_item(self, item, spider):
        self.database.insert_wine(item)
        # self.store_db(item)
        # we need to return the item below as scrapy expects us to!
        return item
