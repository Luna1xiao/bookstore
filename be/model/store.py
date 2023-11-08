import logging
import os
import sys
sys.path.append("D:\\anaconda3\\envs\\env_2023_aut\\lib\\site-packages")
import pymongo


class Store:
    database: str

    def __init__(self, db_path):
        self.database = os.path.join(db_path, "be.db")

    def get_db_conn(self) -> pymongo.database.Database:
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        return self.client["datadb"]


database_instance: Store = None


def init_database(db_path):
    global database_instance
    database_instance = Store(db_path)


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()
