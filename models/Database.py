from datetime import datetime

import pymongo


class Database(object):
    url = 'mongodb://127.0.0.1:27017/'
    # url = 'mongodb+srv://vipKhana:vipKhana@clustervipkhana-hfwa8.mongodb.net/test?retryWrites=true&w=majority'
    db = None

    # --------------------------------DATABASE INITIALIZE METHOD--------------------------------#
    @staticmethod
    def __initialize__():
        client = pymongo.MongoClient(Database.url)
        Database.db = client['mainDB']  # Name of Database

    #
    # --------------------------------FIND METHOD--------------------------------#
    @staticmethod
    def find(collection, query):
        return Database.db[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.db[collection].find_one(query)

    #
    # --------------------------------INSERT METHOD--------------------------------#
    @staticmethod
    def insert(collection, query):
        return Database.db[collection].insert(query)

    #
    # --------------------------------UPDATE METHOD--------------------------------#
    @staticmethod
    def update(collection, query, new_data):
        return Database.db[collection].update(query, new_data)

    #
    # --------------------------------DELETE METHOD--------------------------------#
    @staticmethod
    def delete(collection, query):
        return Database.db[collection].delete_one(query)

    #
    # --------------------------------LOG METHOD--------------------------------#
    @staticmethod
    def add_log(message):
        return Database.db['activity_logs'].insert({"_id": str(datetime.now()), "message": message})
