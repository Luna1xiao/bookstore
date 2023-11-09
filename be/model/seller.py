import logging
import json
from be.model import error
from be.model import store
from pymongo import MongoClient

class Seller:
    def __init__(self):
        self.db = store.get_db_conn()

    def add_book(self,user_id: str,store_id: str,book_id: str,book_json_str: str,stock_level: int, )-> (str, str, str, str, int):
        try:
            user_collection = self.db['user']
            store_collection = self.db['store']

            if not user_collection.find_one({'user_id': user_id}):
                return error.error_non_exist_user_id(user_id)
            if not store_collection.find_one({'store_id': store_id}):
                return error.error_non_exist_store_id(store_id)
            if  store_collection.find_one({'store_id': store_id, 'book.book_id': book_id}):#这里改一下
                return error.error_exist_book_id(book_id)

            book_info = json.loads(book_json_str)
            book_info['book_id'] = book_id

            store_info = {
                'store_id': store_id,
                'book': [
                    {
                        'book_id': book_id,
                        'book_info': book_info,
                        'stock_level': stock_level,
                    }
                ],
                'user_id': user_id,
            }
            store_collection.insert_one(store_info)
        except Exception as e:
            logging.info("Error: {}".format(str(e)))
            return 500, "Internal Server Error"
        return 200, "ok"

    def add_stock_level(
        self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            user_collection = self.db['user']
            store_collection = self.db['store']

            # 检查用户是否存在
            if not user_collection.find_one({'user_id': user_id}):
                return error.error_non_exist_user_id(user_id)
            
            # 检查店铺是否存在
            if not store_collection.find_one({'store_id': store_id}):
                return error.error_non_exist_store_id(store_id)

            # 查找特定书籍
            store_info = store_collection.find_one(
                {'store_id': store_id, 'book.book_id': book_id}
            )
            if not store_info:
                return error.error_non_exist_book_id(book_id)

            # 获取书籍信息列表
            books = store_info.get('book')

            # 找到特定书籍
            for book in books:
                if book.get('book_id') == book_id:
                    stock_level = book.get('stock_level')
                    new_stock_level = stock_level + add_stock_level

                    # 更新库存
                    store_collection.update_one(
                        {
                            'store_id': store_id,
                            'book.book_id': book_id
                        },
                        {
                            '$set': {'book.$.stock_level': new_stock_level}
                        }
                    )

        except Exception as e:
            logging.info("Error: {}".format(str(e)))
            return 500, "Internal Server Error"

        return 200, "ok"

    # def create_store(self, user_id: str, store_id: str) -> (int, str):
    #     try:
    #         user_collection = self.db['user']
    #         user_store_collection = self.db['store']
    #
    #         if not user_collection.find_one({'user_id': user_id}):
    #             return error.error_non_exist_user_id(user_id)
    #         if user_store_collection.find_one({'store_id': store_id}):
    #             return error.error_exist_store_id(store_id)
    #
    #         user_store_info = {
    #             'store_id': store_id,
    #             'user_id': user_id
    #         }
    #         self.db['store'].insert_one(user_store_info)
    #
    #     except Exception as e:
    #         logging.info("Error: {}".format(str(e)))
    #         return 500, "Internal Server Error"
    #
    #     return 200, "ok"

# from pymongo import MongoClient
# import uuid
# import json
# import logging
# from be.model import error
# from be.model import store
# class Seller:
#     def __init__(self, mongo_uri, database_name):
#         self.db = store.get_db_conn()
#
#     def add_book(
#         self,
#         user_id: str,
#         store_id: str,
#         book_id: str,
#         book_json_str: str,
#         stock_level: int,
#     ):
#         try:
#             user_collection = self.db['user']
#             store_collection = self.db['store']
#
#             if not user_collection.find_one({'user_id': user_id}):
#                 return error.error_non_exist_user_id(user_id)
#             if not store_collection.find_one({'store_id': store_id}):
#                 return error.error_non_exist_store_id(store_id)
#             if store_collection.find_one({'store_id': store_id, 'book_id': book_id}):
#                 return error.error_exist_book_id(book_id)
#
#             book_info = json.loads(book_json_str)
#             book_info['book_id'] = book_id
#
#             store_info = {
#                 'store_id': store_id,
#                 'book_id': book_id,
#                 'book_info': json.dumps(book_info),
#                 'stock_level': stock_level
#             }
#             store_collection.insert_one(store_info)
#
#         except Exception as e:
#             logging.info("Error: {}".format(str(e)))
#             return 500, "Internal Server Error"
#
#         return 200, "ok"
#
#     def add_stock_level(
#         self, user_id: str, store_id: str, book_id: str, add_stock_level: int
#     ):
#         try:
#             user_collection = self.db['user']
#             store_collection = self.db['store']
#
#             if not user_collection.find_one({'user_id': user_id}):
#                 return error.error_non_exist_user_id(user_id)
#             if not store_collection.find_one({'store_id': store_id}):
#                 return error.error_non_exist_store_id(store_id)
#             store_info = store_collection.find_one({'store_id': store_id, 'book_id': book_id})
#             if not store_info:
#                 return error.error_non_exist_book_id(book_id)
#
#             stock_level = store_info.get('stock_level')
#             store_collection.update_one(
#                 {'store_id': store_id, 'book_id': book_id},
#                 {'$set': {'stock_level': stock_level + add_stock_level}}
#             )
#
#         except Exception as e:
#             logging.info("Error: {}".format(str(e)))
#             return 500, "Internal Server Error"
#
#         return 200, "ok"
#
#     def create_store(self, user_id: str, store_id: str) -> (int, str):
#         try:
#             user_collection = self.db['user']
#             user_store_collection = self.db['store']
#
#             if not user_collection.find_one({'user_id': user_id}):
#                 return error.error_non_exist_user_id(user_id)
#             if user_store_collection.find_one({'store_id': store_id}):
#                 return error.error_exist_store_id(store_id)
#
#             user_store_info = {
#                 'store_id': store_id,
#                 'user_id': user_id
#             }
#             user_store_collection.insert_one(user_store_info)
#
#         except Exception as e:
#             logging.info("Error: {}".format(str(e)))
#             return 500, "Internal Server Error"
#
#         return 200, "ok"
#

    # 添加了店铺的balance
    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            user_collection = self.db['user']
            user_store_collection = self.db['store']

            if not user_collection.find_one({'user_id': user_id}):
                return error.error_non_exist_user_id(user_id)
            if user_store_collection.find_one({'store_id': store_id}):
                return error.error_exist_store_id(store_id)

            user_store_info = {
                'store_id': store_id,
                'user_id': user_id
            }
            self.db['store'].insert_one(user_store_info)

        except Exception as e:
            logging.info("Error: {}".format(str(e)))
            return 500, "Internal Server Error"
        return 200, "ok"

    # 发货
    def send_books(self, store_id: str, order_id: str) -> (int, str):
        try:
            if not self.db['store'].find_one({'store_id': store_id}):
                return error.error_non_exist_store_id(store_id)
            if not self.db['history_order'].find_one({'order_id': order_id}):
                return error.error_invalid_order_id(order_id)

            order = self.db['history_order'].find_one({'order_id': order_id})

            if order["status"] != 2:
                return 500, "Invalid order status"

            #self.db["history_order"].upadte_one({"order_id": order_id}, {"$set": {"status": 3}})
            self.db["history_order"].update_one({"order_id": order_id}, {"$set": {"status": 3}})



        except Exception as e:
            logging.info("Error: {}".format(str(e)))
            return 500, "Internal Server Error"

        return 200, "ok"
