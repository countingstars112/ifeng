# coding: utf-8

import pymongo
class MongoDB(object):
    def __init__(self):
        client = pymongo.MongoClient('182.150.37.55', 50070)
        db = client['news']
        # client = pymongo.MongoClient('127.0.0.1', 27017)
        # db = client['ifend']
        self.collection_zhengwen = db['content']
        self.collection_comment = db['comment']

    def put_content(self, value):
        return self.collection_zhengwen.save(value)

    def put_comment(self, value):
        return self.collection_comment.save(value)

    def update(self, value):
        return self.collection_zhengwen.update_one()