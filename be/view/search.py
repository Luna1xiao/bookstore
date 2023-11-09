from flask import Blueprint
from flask import request
from flask import jsonify
from be.model import search

bp_search = Blueprint("search", __name__, url_prefix="/search")

@bp_search.route("/search_in_store", methods=["POST"])
def search_in_store():
    choose: int = request.json.get("choose")
    store_id: str = request.json.get("store_id")
    keyword: str = request.json.get("keyword")
    page: int = request.json.get("page")
    limit: int = request.json.get("limit")
    search_instance = search.Search()
    code, result, message = search_instance.search_in_store(choose, store_id, keyword, page, limit)
    #return  code,jsonify({"message": message})
    return jsonify({"message": message, "result": result}), code

@bp_search.route("/search_all", methods=["POST"])
def search_all():
    choose: int = request.json.get("choose")
    keyword: str = request.json.get("keyword")
    page: int = request.json.get("page")
    limit: int = request.json.get("limit")
    search_instance = search.Search()
    code, result,message = search_instance.search_all(choose, keyword, page, limit)
    return jsonify({"message": message, "result": result}), code
