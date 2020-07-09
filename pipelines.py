# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class TubaotuScrapyProjectPipeline:
    def __init__(self):
        myclient = pymongo.MongoClient("mongodb://81.68.119.98:27017")
        mydb = myclient['db_tubatu']
        self.mycollection = mydb['collection_tubatu']

    def process_item(self, item, spider):
        data = dict(item)
        self.mycollection.insert_one(data)
        return item
