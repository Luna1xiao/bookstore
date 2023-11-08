import uuid
import logging
from be.model import db_conn
from be.model import error
import sys
sys.path.append("D:\\anaconda3\\envs\\env_2023_aut\\lib\\site-packages")
from pymongo.errors import PyMongoError
import re


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)



    def new_order(
            self, user_id: str, store_id: str, id_and_count: [(str, int)]
    ) -> (int, str, str):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))
            count1=0
            print(0)
            for book_id, count in id_and_count:
                query = {"store_id": store_id, "book.book_id": book_id}
                row = self.db['store'].find_one(query)
                print(1)
                if row is None:
                    # 如果找不到匹配的书籍，返回错误
                    return error.error_non_exist_book_id(book_id) + (order_id,)

                # 获取匹配文档中的书籍信息和库存级别


                # 找到 book_id 对应的索引
                index = -1
                for i, book in enumerate(row['book']):
                    if book['book_id'] == book_id:
                        index = i
                        break
                if index == -1:
                    # 如果找不到 book_id，返回错误
                    return error.error_non_exist_book_id(book_id) + (order_id,)
                print(3)
                book_info = row['book'][index]['book_info']
                stock_level = row['book'][index]['stock_level']
                print(2)

                # 在这里可以继续处理库存级别（例如，检查库存是否足够）
                print(stock_level)
                print(type(stock_level))
                #stock_level = stock_levels[index]

                print(f"Stock level for book_id {book_id}: {stock_level}")
                price=row['book'][index]['book_info']['price']
                print(price)

                # # 在这里可以继续处理 book_info（例如，提取价格等）
                # match = re.search(r'"price": (\d+)', book_info)
                # if match:
                #     price = match.group(1)
                #     print(f"The price is: {price}")

                # 打印提取出的"price"字段的内容
                # print(price)
                print(stock_level, count)
                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)

                stock_level-= count

                # 更新数据库中的库存级别
                update = {"$set": {"book.{0}.stock_level".format(index): stock_level}}
                result = self.db['store'].update_one(query, update)
                # if result.modified_count == 0:
                #     return error.error_stock_level_low(book_id) + (order_id,)
                # 插入订单详细信息
                order_detail = {
                    "id": book_id,
                    "count": count,
                    "price": price
                }
                self.db['order'].update_one(
                    {"order_id": uid, "store_id": store_id, "user_id": user_id},
                    {"$push": {"book": order_detail}},
                    upsert=True
                )
                print(5)

            order_id = uid
            print(order_id)
        except PyMongoError as e:
            return 528, str(e), ""
        except BaseException as e:
            return 530, str(e), ""

        return 200, "ok", order_id



    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):

        try:
            # 执行MongoDB查询
            query = {"order_id": order_id}
            result = self.db['order'].find_one(query)

            if result is None:
                return error.error_invalid_order_id(order_id)

            order_id = result["order_id"]
            buyer_id = result["user_id"]
            store_id = result["store_id"]

            if buyer_id != user_id:
                print(1)
                return error.error_authorization_fail()

            user_query = {"user_id": buyer_id}
            user_result = self.db['user'].find_one(user_query)

            if user_result is None:
                return error.error_non_exist_user_id(buyer_id)

            user_balance = user_result.get("balance")
            user_password = user_result.get("password")
            print(user_password)
            print(password)

            if password != user_password:
                return error.error_authorization_fail()

            # 执行MongoDB查询
            user_store_query = {"store_id": store_id}
            user_store_result = self.db['store'].find_one(user_store_query)

            if user_store_result is None:
                return error.error_non_exist_store_id(store_id)

            seller_id = user_store_result.get("user_id")

            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            order_detail_query = {"order_id": order_id}
            order_detail_cursor = self.db['order'].find(order_detail_query)
            print("查找好了order")

            total_price = 0


            for order_doc in order_detail_cursor:
                # 从订单文档中的book字段获取书籍数组
                book_array = order_doc.get('book', [])
                # 遍历书籍数组中的每本书
                for book in book_array:
                    # 从书籍对象中获取数量和价格
                    count = int(book.get('count', 0))
                    price = int(book.get('price', 0)) # 将价格转换为浮点数，以便进行乘法计算

                    # 计算每本书的总价并将其累加到总价中
                    book_total = count * price
                    total_price += book_total

            print("过了price")

            user_collection = self.db["user"]  # 替换为实际的用户集合名称
            user_query = {"user_id": buyer_id}
            user_result = user_collection.find_one(user_query)

            if user_result is None:
                return error.error_non_exist_user_id(buyer_id)

            user_balance = user_result.get("balance")

            if user_balance < total_price:
                return error.error_not_sufficient_funds(order_id)

            update_query = {
                "user_id": buyer_id,
                "balance": {"$gte": total_price}
            }
            update_update = {
                "$inc": {"balance": -total_price}
            }
            result = user_collection.update_one(update_query, update_update)

            if result.modified_count == 0:
                return error.error_not_sufficient_funds(order_id)

            # 执行MongoDB更新
            update_query = {
                "user_id": buyer_id
            }
            update_update = {
                "$inc": {"balance": total_price}
            }
            result = user_collection.update_one(update_query, update_update)

            if result.matched_count == 0:
                return error.error_non_exist_user_id(buyer_id)


            delete_query = {"order_id": order_id}
            result = self.db['order'].delete_one(delete_query)

            if result.deleted_count == 0:
                return error.error_invalid_order_id(order_id)

            #这里是原本的order_detail不用了

        except PyMongoError as e:
            return 528, str(e), ""

        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        try:
            # 执行MongoDB查询
            query = {"user_id": user_id}
            result = self.db['user'].find_one(query)

            if result is None:
                return error.error_authorization_fail()

            if result["password"] != password:
                return error.error_authorization_fail()

            # 执行MongoDB更新
            update_query = {"$inc": {"balance": add_value}}
            result = self.db['user'].update_one({"user_id": user_id}, update_query)

            if result.modified_count == 0:
                return error.error_non_exist_user_id(user_id)

        except PyMongoError as e:
            error_code = 528  # 替换为适当的错误代码
            error_message = str(e)
            logging.info(f"{error_code}, {error_message}")
            return error_code, error_message

        except Exception as e:
            error_code = 530  # 替换为适当的错误代码
            error_message = str(e)
            logging.info(f"{error_code}, {error_message}")
            return error_code, error_message

        return 200, "ok"
    

    # 收货
    def receive_books(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.db['history_order'].find_one({'order_id': order_id}):
                return error.error_invalid_order_id(order_id)
            
            user = self.db['user'].find_one({'user_id': user_id})
            if user['password'] != password:
                return error.error_authorization_fail()

            order = self.db['history_order'].find_one({'order_id': order_id})
            if order['user_id'] != user_id:
                return error.error_authorization_fail()
            if order['status'] != 3:
                return 500, "Invalid order status"
            
            # 给卖家增加balance
            total_price = 0
            for order_doc in order.get('order', []):
                book_array = order_doc.get('book', [])
                for book in book_array:
                    count = int(book.get('count', 0))
                    price = int(book.get('price', 0))

                    book_total = count * price
                    total_price += book_total

            store = self.db['store'].find_one({'store_id': order['store_id']})
            seller_id = store['user_id']
            self.db["users"].update_one({"user_id": seller_id}, {"$inc": {"balance": total_price}})

            self.db["history_order"].update_one({"order_id": order_id}, {"$set": {"status": 4}})

        except Exception as e:
            logging.info("Error: {}".format(str(e)))
            return 500, "Internal Server Error"
        return 200, "OK"
        