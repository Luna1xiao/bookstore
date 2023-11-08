import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
import uuid


class TestDeliverBooks:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_deliver_books_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_deliver_books_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_deliver_books_buyer_id_{}".format(str(uuid.uuid1()))
        self.buyer_password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.buyer_password)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        self.seller = self.gen_book.get_seller()
        yield

    # 发货测试
    def test_send_books_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        code = self.buyer.add_funds(100000000)
        assert code == 200
        code = self.buyer.payment(order_id)
        assert code == 200
        code = self.seller.send_books(self.store_id,order_id)
        assert code == 200

    def test_send_status_error(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        code = self.seller.send_books(self.store_id,order_id)
        assert code != 200

    def test_send_non_exist_order_id(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        code = self.buyer.add_funds(100000000)
        assert code == 200
        code = self.buyer.payment(order_id)
        assert code == 200
        code = self.seller.send_books(self.store_id, order_id + "invalid")
        assert code != 200

    def test_send_non_exist_store_id(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        code = self.buyer.add_funds(100000000)
        assert code == 200
        code = self.buyer.payment(order_id)
        assert code == 200
        code = self.seller.send_books(self.store_id + "invalid", order_id)
        assert code != 200

    # 收货测试
    def test_receive_books_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        code = self.buyer.add_funds(100000000)
        assert code == 200
        code = self.buyer.payment(order_id)
        assert code == 200
        code = self.seller.send_books(self.store_id,order_id)
        assert code == 200
        code = self.buyer.receive_books(self.buyer_id, self.buyer_password, order_id)
        assert code == 200

    def test_receive_status_error(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        code = self.buyer.receive_books(self.buyer_id, self.buyer_password, order_id)
        assert code != 200

    def test_receive_non_exist_order_id(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        code = self.buyer.add_funds(100000000)
        assert code == 200
        code = self.buyer.payment(order_id)
        assert code == 200
        code = self.seller.send_books(self.store_id,order_id)
        assert code == 200
        code = self.buyer.receive_books(self.buyer_id, self.buyer_password, order_id + "invalid")
        assert code != 200

    def test_receive_non_exist_buyer_id(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        code = self.buyer.add_funds(100000000)
        assert code == 200
        code = self.buyer.payment(order_id)
        assert code == 200
        code = self.seller.send_books(self.store_id,order_id)
        assert code == 200
        code = self.buyer.receive_books(self.buyer_id + "invalid", self.buyer_password, order_id)
        assert code != 200

    def test_receive_wrong_password(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        code = self.buyer.add_funds(100000000)
        assert code == 200
        code = self.buyer.payment(order_id)
        assert code == 200
        code = self.seller.send_books(self.store_id,order_id)
        assert code == 200
        code = self.buyer.receive_books(self.buyer_id, self.buyer_password + "invalid", order_id)
        assert code != 200