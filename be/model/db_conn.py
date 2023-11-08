from be.model import store


class DBConn:
    def __init__(self):
        self.db = store.get_db_conn()

    def user_id_exist(self, user_id):
        query = {"user_id": user_id}
        result = self.db["user"].find_one(query)
        return result is not None

    def book_id_exist(self, store_id, book_id):
        query = {"store_id": store_id, "book.book_id": book_id}
        result = self.db["store"].find_one(query)
        return result is not None

    def store_id_exist(self, store_id):
        query = {"store_id": store_id}
        result = self.db["store"].find_one(query)
        return result is not None
