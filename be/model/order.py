from be.model import db_conn
from sqlalchemy.exc import SQLAlchemyError
from be.model import error

class Order(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def cancel_order(self, order_id, end_status=0):
            try:
                # 查询订单信息并删除
                order = self.db['order'].find_one_and_delete({"order_id": order_id})
                if not order:
                    return error.error_invalid_order_id(order_id)

                # 处理订单数据
                order['status'] = 0


                books = []
                for book_data in order['books']:
                    book_id = book_data['book_id']
                    count = book_data['count']

                    # 更新库存

                    result = self.db['store'].update_one(
                        {"store_id": order['store_id'], "user_id": order['user_id'], "book.book_id": book_id},
                        {"$inc": {"book.stock_level": count}}
                    )
                    if result.modified_count == 0:
                        return error.error_non_exist_book_id(book_id) + (order_id,)
                    books.append(book_data)

                order['books'] = books

                # 插入已取消订单
                self.db['history_order'].insert_one(order)

                return 200, "ok"

            except Exception as e:
                return 528, str(e)


