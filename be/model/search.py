from pymongo.errors import PyMongoError
from be.model import db_conn
from be.model import error
from urllib.parse import urljoin
import pymongo


class Search(db_conn.DBConn):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["datadb"]

    def search_in_store(self, choose: int, store_id:str,keyword: str, page: int, limit: int,):
        order_id = ""
        try:
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)

            # 构建查询条件
            choose = int(choose)
            page = int(page)
            limit = int(limit)
            skip_count = (page - 1) * limit

            if choose == 0:
                search_query = self.db["store"].find({
                    "$and": [
                        {"store_id": store_id},
                        {"book.book_info.title": {"$regex": keyword}}
                    ]
                }).skip(skip_count).limit(limit)
            elif choose == 1:
                search_query = self.db["store"].find({
                    "$and": [
                        {"store_id": store_id},
                        {"book_info.tags": {"$regex": keyword}}
                    ]
                }).skip(skip_count).limit(limit)
            elif choose == 2:
                search_query = self.db["store"].find({
                    "$and": [
                        {"store_id": store_id},
                        {"book_info.content": {"$regex": keyword}}
                    ]
                }).skip(skip_count).limit(limit)
            elif choose == 3:
                search_query = self.db["store"].find({
                    "$and": [
                        {"store_id": store_id},
                        {"book_info.book_intro": {"$regex": keyword}}
                    ]
                }).skip(skip_count).limit(limit)

            self.db['store'].create_index([("book_info.title", 1)])
            self.db['store'].create_index([("book_info.tags", 1)])
            self.db['store'].create_index([("book_info.content", 1)])
            self.db['store'].create_index([("book_info.book_intro", 1)])

            result = []
            for doc in search_query:
                if "book" in doc and isinstance(doc["book"], list):
                    for book in doc["book"]:
                        if "book_info" in book and "title" in book["book_info"]:
                            title = book["book_info"]["title"]
                            content = book["book_info"].get("content", "")
                            author = book["book_info"]["author"]
                            book_intro = book["book_info"]["book_intro"]
                            tags = book["book_info"].get("tags", [])

                            book_data = {
                                "title": title,
                                "author": author,
                                "book_intro": book_intro,
                                "content": content,
                                "tags": tags
                            }
                            result.append(book_data)
                        else:
                            print("Not found in this document")
                else:
                    print("No 'book' array found in this document")

            return 200, "ok", result
        except PyMongoError as e:
            return 528, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []


    def search_all(self, choose: int, keyword: str, page: int, limit: int,):
        try:
            choose = int(choose)
            page = int(page)
            limit = int(limit)
            skip_count = (page - 1) * limit

            if choose == 0:
                search_query = self.db["store"].find({
                    "book.book_info.title": {"$regex": keyword}
                }).skip(skip_count).limit(limit)
            elif choose == 1:
                search_query = self.db["store"].find({
                        "book_info.tags": {"$regex": keyword}
                }).skip(skip_count).limit(limit)
            elif choose == 2:
                search_query = self.db["store"].find({
                        "book_info.content": {"$regex": keyword}
                }).skip(skip_count).limit(limit)
            elif choose == 3:
                search_query = self.db["store"].find({
                        "book_info.book_intro": {"$regex": keyword}
                }).skip(skip_count).limit(limit)

            self.db['store'].create_index([("book_info.title", 1)])
            self.db['store'].create_index([("book_info.tags", 1)])
            self.db['store'].create_index([("book_info.content", 1)])
            self.db['store'].create_index([("book_info.book_intro", 1)])

            result = []
            for doc in search_query:
                if "book" in doc and isinstance(doc["book"], list):
                    for book in doc["book"]:
                        if "book_info" in book and "title" in book["book_info"]:
                            title = book["book_info"]["title"]
                            content = book["book_info"].get("content", "")
                            author = book["book_info"]["author"]
                            book_intro = book["book_info"]["book_intro"]
                            tags = book["book_info"].get("tags", [])

                            book_data = {
                                "title": title,
                                "author": author,
                                "book_intro": book_intro,
                                "content": content,
                                "tags": tags
                            }
                            result.append(book_data)
                        else:
                            print("Not found in this document")
                else:
                    print("No 'book' array found in this document")

            return 200, "ok", result
        except PyMongoError as e:
            return 528, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []



# if __name__ == "__main__":
#     # 创建Search类的实例
#     search_instance = Search()
#
#     # 调用init方法
#     #search_instance.init()
#
#     # 调用search_in_store方法
#     choose = 0  # 你需要提供合适的参数值
#     store_id = "test_send_books_store_id_f55ce92d-7c70-11ee-8202-a87eeabd0915"  # 你需要提供合适的参数值
#     keyword = "红"  # 你需要提供合适的参数值
#     page = 1  # 你需要提供合适的参数值
#     limit = 10  # 你需要提供合适的参数值
#     response = search_instance.search_all(choose, keyword, page, limit)
#
#     # 处理返回的结果
#     status_code, message, result = response
#     if status_code == 200:
#         print("Search successful:")
#         for book_data in result:
#             print(book_data)
#     else:
#         print(f"Search failed - Status Code: {status_code}, Message: {message}")


