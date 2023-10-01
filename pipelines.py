import json
from db_manager import Database


class SavingToDatabasePipeline(object):
    def __init__(self):
        self.database = Database()

    def process_item(self, item, spider):
        self.database.insert_wine(item)
        # we need to return item as scrapy expects us to
        return item


class SaveJSONPipeline:
    def __init__(self):
        self.file = open('result.json', 'w')

    def process_item(self, item, spider):
        # calling dumps to create json data.
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
