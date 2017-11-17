from time import time
from os import path
from typing import List, DefaultDict
from pymongo import MongoClient, collection
from collections import defaultdict
from inspect import currentframe, getframeinfo
from ..Logger import log
from traceback import format_tb
from .crawler import dump_pickle, load_pickle
from datetime import datetime


def read_path(filename):
    with open(filename, 'r') as file:
        server_path = file.read()
    return server_path

Article = DefaultDict
Articles = List[Article]


class Mongodb:
    def __init__(self, hash_check=True):
        self.server_path = read_path(path.join(path.dirname(__file__), 'server_path.txt'))
        self.client = MongoClient(self.server_path, 27017)
        self.db = self.client.test
        if hash_check:
            self.hash = self.db_hash()

    def create_col(self, c_name: str) -> None:
        collection.Collection(self.db, c_name, create=True)

    def count_all(self, col_name: str) -> int:
        return self.db[col_name].find({}).count()

    def insert_one(self, col_name: str, doc: Article) -> None:
        result = self.db[col_name].insert_one(doc)
        log(getframeinfo(currentframe()), 'DB insert result : ', result.inserted_id)

    def insert_many(self, col_name: str, docs: Articles) -> None:
        result = self.db[col_name].insert_many([doc for doc in docs if doc is not None])
        log(getframeinfo(currentframe()), 'DB insert result : ', result.inserted_ids)

    def search_title(self, col_name: str, query: str) -> Articles:
        start = time()
        docs = self.db[col_name].find({'title': {'$regex': ".*" + query + ".*"}})
        if not docs:
            log(getframeinfo(currentframe()), 'Collection does not exist or no doc match.')
            return []
        lst = list(docs)
        log(getframeinfo(currentframe()), 'Query : ', query, ' total : ', str(len(lst)))
        log(getframeinfo(currentframe()), 'Spent time : ', str(time() - start)[0:5], ' secs')
        return lst

    def search_label(self, col_name: str, query: str ="雷") -> Articles:
        start = time()
        docs = self.db[col_name].find({'label': {'$regex': ".*" + query + ".*"}})
        if not docs:
            log(getframeinfo(currentframe()), 'Collection does not exist or no doc match.')
            return []
        lst = list(docs)
        log(getframeinfo(currentframe()), 'Query : ', query, ' total : ', str(len(lst)))
        log(getframeinfo(currentframe()), 'Spent time : ', str(time() - start)[0:5], ' secs')
        return lst

    def search_any(self, col_name: str, field: str, query: str) -> Articles:
        start = time()
        docs = self.db[col_name].find({field: {'$regex': ".*" + query + ".*"}})
        if not docs:
            log(getframeinfo(currentframe()), 'Collection does not exist or no doc match.')
            return []
        lst = list(docs)
        log(getframeinfo(currentframe()), 'Query : ', query, ' in ', field, ' total : ', str(len(lst)))
        log(getframeinfo(currentframe()), 'Spent time : ', str(time() - start)[0:5], ' secs')
        return lst

    def search_date(self, col_name: str, month: int, year: int, query: str) -> int:
        big_month = [1, 3, 5, 7, 8, 10, 12]
        if month in big_month:
            date = 31
        elif month == 2:
            date = 28
        else:
            date = 30
        start = datetime(year, month, 1)
        end = datetime(year, month, date)
        docs = self.db[col_name].find({'title': {'$regex': ".*" + query + ".*"}, 'date': {'$lt': end, '$gte': start}})
        return docs.count()

    def search_dual(self, col_name: str, field1: str, query: str, field2: str, score: int) -> Articles:
            start = time()
            docs = self.db[col_name].find_one({
                field1: {'$regex': ".*" + query + ".*"},
                field2: score,
                'modified': False
            })
            if not docs:
                log(getframeinfo(currentframe()), 'Collection does not exist or no doc match.')
                return []
            log(getframeinfo(currentframe()), 'Spent time : ', str(time() - start)[0:5], ' secs')
            return docs

    def search_encode(self, col_name: str, query: str) -> Articles:
        start = time()
        docs = self.db[col_name].find({'title': {'$regex': ".*" + query + ".*"}}, {'encode': 1})
        if not docs:
            log(getframeinfo(currentframe()), 'Collection does not exist or no doc match.')
            return []
        lst = list(docs)
        log(getframeinfo(currentframe()), 'Query : ', query, ' in title total : ', str(len(lst)))
        log(getframeinfo(currentframe()), 'Spent time : ', str(time() - start)[0:5], ' secs')
        return lst

    def db_all(self, col_name: str) -> Articles:
        start = time()
        try:
            pickle_all = load_pickle(col_name)
            pickle_hash = load_pickle('hash')
            if pickle_hash['collections'][col_name] == self.hash['collections'][col_name]:
                log(getframeinfo(currentframe()), 'Fetch data from pickle file : ', col_name)
                return pickle_all
        except FileNotFoundError:
            pass
        docs = self.db[col_name].find({})
        if not docs:
            log(getframeinfo(currentframe()), 'Collection does not exist or empty.')
            return []
        lst = list(docs)
        dump_pickle(col_name, lst)
        dump_pickle('hash', self.hash)
        log(getframeinfo(currentframe()), 'Total : ', str(len(lst)))
        log(getframeinfo(currentframe()), 'Spent time : ', str(time() - start)[0:5], ' secs')
        return lst

    def db_hash(self) -> DefaultDict:
        return self.db.command('dbHash')

    def greater(self, col_name: str, score) -> Articles:
        docs = self.db[col_name].find({'score': {'$gt': score}})
        lst = list(docs)
        if lst is None:
            log(getframeinfo(currentframe()), 'This collection does not exist score filed')
            raise TypeError
        return lst

    def update_one_filed(self, col_name: str, _id: str, field: str, docs) -> None:
        result = self.db[col_name].update_one({'_id': _id}, {'$set': {field: docs}})
        log(getframeinfo(currentframe()), 'Update result : ', result.matched_count)

    def update_one(self, col_name: str, _id: str, segments, pos) -> None:
        result = self.db[col_name].update_one({'_id': _id}, {'$set': {'segments': segments, 'pos': pos}})
        log(getframeinfo(currentframe()), 'Update result : ', result.matched_count)

    def update_score(self, col_name: str, _id: str, score: int) -> None:
        self.db[col_name].update_one({'_id': _id}, {'$set': {'score': score}})

    def update_all_score(self, col_name: str, labels) -> None:
        docs = self.db_all(col_name)

        for index, doc in enumerate(docs):
            self.update_score(col_name, doc['_id'], labels[doc['label']] if doc['label'] in labels else -1)
            if index % 1000 == 0:
                log(getframeinfo(currentframe()), '1000 articles updated.')

        log(getframeinfo(currentframe()), 'All articles updated!')

    def update_modify(self):
        self.db['articles'].update_many({}, {'$set': {'modified': False}})
        log(getframeinfo(currentframe()), 'All articles updated modify field!')

    def update_modified(self, _id):
        self.db['articles'].update_one({'_id': _id}, {'$set': {'modified': True}})
        log(getframeinfo(currentframe()), 'All articles updated modify field!')

    def delete_one(self, col_name: str, _id: str) -> None:
        result = self.db[col_name].delete_one({'_id': _id})
        log(getframeinfo(currentframe()), 'Deleted ', str(result))

    def close(self) -> None:
        self.client.close()

    def label_view(self):
        labels = defaultdict(int)
        for article in self.search_label("articles"):
            if article['label'] != article['title']:
                labels[article['label']] += 1
        return labels

    # last is last article index, require is how much articles you need.
    def num_articles(self, col_name: str, last: int, require: int):
        start = time()
        docs = self.db[col_name].find({}).skip(last).limit(require)
        if not docs:
            log(getframeinfo(currentframe()), 'Collection does not exist or empty.')
            return []
        lst = list(docs)
        log(getframeinfo(currentframe()), 'Total : ', str(len(lst)))
        log(getframeinfo(currentframe()), 'Spent time : ', str(time() - start)[0:5], ' secs')
        return lst

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            log(getframeinfo(currentframe()), 'Error type : ', str(exc_type))
            log(getframeinfo(currentframe()), 'Error : ', str(exc_val))
            log(getframeinfo(currentframe()), 'Error tb : \n', ''.join(format_tb(exc_tb)))
        self.client.close()
        log(getframeinfo(currentframe()), 'Database connection closed...')
        return True
