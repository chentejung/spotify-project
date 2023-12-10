import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
import urllib
import bson

def connectDB():
    userName = urllib.parse.quote(os.getenv('DB_ROOT_USERNAME'))
    userPass = urllib.parse.quote(os.getenv('DB_ROOT_PASSWORD'))
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbName = os.getenv('DB_NAME')
    client = MongoClient(f'mongodb://{userName}:{userPass}@{host}:{port}')
    return client[dbName]


def buildeCollection(colName):
    return connectDB()[colName]

class Spotify:
    def __init__(self, colName):
        self.colName = colName
        self.collection = buildeCollection(colName)

    def insert_one(self, data):
        return self.collection.insert_one(data)
    
    def insert_many(self, data):
        return self.collection.insert_many(data)
    
    def update_one(self, srcItem, oriValue, newValue):
        oriItem = {srcItem: oriValue}
        newItem = {"$set" : {srcItem: newValue}}
        return self.collection.update_one(oriItem, newItem)
    
    def get_collection_search_by_id_name(self, srcItem):
        query = {"id": srcItem}
        return self.collection.find_one(query)
    
    def get_collection_search_query(self, colName, srcItem):
        query = {colName: srcItem}
        return self.collection.find_one(query)

    def get_collection_search_query_many(self, query):
        return self.collection.find(query)
    
    def get_collection_search_query_multiple_conditions(self, query, type):
        srcQuery = {
            f'${type}': [query]
        }
        return self.collection.find(srcQuery)
    
    def get_collection_search_specific_columns(self, colName):
        srcDict = {'_id':0}
        for i in colName:
            srcDict[i] = 1
        return self.collection.find({}, srcDict)
    
    def aggregate_number_search(self, srcCol, sortType, filtquery = None):
        srcItem = '$'+srcCol
        if sortType == 'count':
            sortCol2 = '$sum'

        if filtquery != None:
            
            # need to adjust if-else
            col2 = '$'+list(filtquery.keys())[0]
            
            # need to define name as an operator
            pipeline = [
                {"$match": filtquery},
                {"$group": {'_id': srcItem, 'name': {"$first": col2}, sortType: {sortCol2: 1}}},
                {"$sort": bson.SON([(sortType, -1)])}
                ]
        else:
            pipeline = [
                {"$group": {'_id': srcItem, sortType: {sortCol2: 1}}},
                {"$sort": bson.SON([(sortType, -1)])}
                ]
        return self.collection.aggregate(pipeline)
    
    def sort_search(self, srcItem, sort=None):
        if sort == 'asc':
            sort = None
        elif sort == 'desc':
            sort = -1
        return self.collection.find().sort(srcItem, sort)
    
    def delete_one_by_id_name(self, srcItem):
        query = {"id": srcItem}
        return self.collection.delete_one(query)