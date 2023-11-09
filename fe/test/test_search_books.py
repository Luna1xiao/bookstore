import pytest
import uuid
from be.model.search import Search
from fe.access.new_seller import register_new_seller


class TestSearchBooks:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.sch = Search()
        self.seller_id = "test_add_books_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_add_books_store_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        # self.seller = register_new_seller(self.seller_id, self.password)
        # code = self.seller.create_store(self.store_id)
        # assert code == 200
        self.keyword = "三毛"
        self.page = 1
        self.limit = 10
        yield

    # def test_error_exist_store_id(self):
    #     self.seller = register_new_seller(self.seller_id, self.password)
    #     code = self.seller.create_store(self.store_id)
    #     assert code == 200
    #     code = self.seller.create_store(self.store_id)
    #     assert code != 200

    def test_search__title_in_store(self):
        self.choose = 0
        self.seller = register_new_seller(self.seller_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200
        code, message, result = self.sch.search_in_store(self.choose, self.store_id, self.keyword, self.page, self.limit)
        assert code == 200

    def test_search_tags_in_store(self):
        self.choose = 1
        self.seller = register_new_seller(self.seller_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200
        code, message, result = self.sch.search_in_store(self.choose, self.store_id, self.keyword, self.page, self.limit)
        assert code == 200

    def test_search_content_in_store(self):
        self.choose = 2
        self.seller = register_new_seller(self.seller_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200
        code, message, result = self.sch.search_in_store(self.choose, self.store_id, self.keyword, self.page, self.limit)
        assert code == 200

    def test_search_book_intro_in_store(self):
        self.choose = 3
        self.seller = register_new_seller(self.seller_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200
        code, message, result = self.sch.search_in_store(self.choose, self.store_id, self.keyword, self.page, self.limit)
        assert code == 200

    def test_search__title_in_store_error(self):
        self.choose = 0
        code, message, result = self.sch.search_in_store(self.choose, self.store_id, self.keyword, self.page, self.limit)
        assert code == 513

    def test_search_tags_in_store_error(self):
        self.choose = 1
        code, message, result = self.sch.search_in_store(self.choose, self.store_id, self.keyword, self.page, self.limit)
        assert code == 513

    def test_search_content_in_store_error(self):
        self.choose = 2
        code, message, result = self.sch.search_in_store(self.choose, self.store_id, self.keyword, self.page, self.limit)
        assert code == 513

    def test_search_book_intro_in_store_error(self):
        self.choose = 3
        code, message, result = self.sch.search_in_store(self.choose, self.store_id, self.keyword, self.page, self.limit)
        assert code == 513

    def test_search__title_all(self):
        self.choose = 0
        code, message, result = self.sch.search_all(self.choose, self.keyword, self.page, self.limit)
        assert code == 200

    def test_search_tags_all(self):
        self.choose = 1
        code, message, result = self.sch.search_all(self.choose, self.keyword, self.page, self.limit)
        assert code == 200

    def test_search_content_all(self):
        self.choose = 2
        code, message, result = self.sch.search_all(self.choose, self.keyword, self.page, self.limit)
        assert code == 200

    def test_search_book_intro_all(self):
        self.choose = 3
        code, message, result = self.sch.search_all(self.choose, self.keyword, self.page, self.limit)
        assert code == 200


if __name__ == "__main__":
    pytest.main()


