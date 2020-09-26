from flask import Blueprint, json, jsonify, request
from flaskr import db
from flaskr.models.stock import Stock, Stock_schema
from marshmallow import ValidationError

# 资源路由
from flask.views import MethodView

stock_bp = Blueprint('stock_bp', __name__, url_prefix='/stock_bp')


class StockAPI(MethodView):

  def get(self):
    dict_request = request.values.to_dict()
    # 序列化数据
    schema = Stock_schema(many=True)
    # sql语句
    sql = Stock.query.order_by(Stock.id.desc())
    # 筛选
    # if dict_request.__contains__('materiel_name'):  sql = sql.filter(Materiel.materiel_name.like('%'+dict_request['materiel_name']+'%')) 
    # if dict_request.__contains__('standard'):       sql = sql.filter(Materiel.standard.like('%'+dict_request['standard']+'%')) 
    # if dict_request.__contains__('unit'):           sql = sql.filter(Materiel.unit.like('%'+dict_request['unit']+'%')) 
    # 物料种类
    if set(['page', 'limit']).issubset(dict_request):
      # 页码
      list_paginate = [
        int(dict_request['page']), 
        int(dict_request['limit'])
      ]
      Pagination = sql.paginate(*list_paginate) # 分页查询
      return jsonify({
        'data': schema.dump(Pagination.items),
        'total': Pagination.total
      })
    else: 
      list_data = sql.all() # 查所有
      return jsonify({
        'data': schema.dump(list_data),
      })

  def post(self):
    pass



stock_view = StockAPI.as_view('stock_api')
stock_bp.add_url_rule('/list', view_func=stock_view, methods=['GET'])
stock_bp.add_url_rule('/create', view_func=stock_view, methods=['POST'])