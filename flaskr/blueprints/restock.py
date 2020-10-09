from flask import Blueprint, json, jsonify, request
from flaskr import db
from decimal import *
# 模型
from flaskr.models.stock import Stock, Stock_schema
from flaskr.models.batch_in import Batch_in, Batch_in_schema
from flaskr.models.materiel import Materiel
# 报错
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

# 资源路由
from flask.views import MethodView

restock_bp = Blueprint('restock', __name__, url_prefix='/restock')


class RestockAPI(MethodView):

  '''进货列表'''
  def get(self):
    dict_request = request.values.to_dict()
    # 序列化数据
    schema = Batch_in_schema(many=True)
    # sql语句
    sql = Batch_in.query.order_by(Batch_in.id.desc())
    # 筛选
    if dict_request.__contains__('stock_id'):  sql = sql.filter(Batch_in.stock_id == dict_request['stock_id']) 
    # 物料种类
    if set(['page', 'limit']).issubset(dict_request):
      # 页码
      list_paginate = [
        int(dict_request['page']),
        int(dict_request['limit'])
      ]
      # Pagination = sql.outerjoin(Stock, Batch_in.stock_id == Stock.id).outerjoin(Materiel, Stock.materiel_id == Materiel.id).paginate(*list_paginate) # 分页查询
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

    
  '''入库'''
  def post(self):
    request_data = request.json
    for index in range(len(request_data['restockNumberTable'])):
      item = request_data['restockNumberTable'][index]
      # 写入or更新库存 --->
      # TODO: 用关联关系一次性写入两个表
      stock_data = {
        'price'       : item['sum'],
        'in_number'   : item['in_number'],
        'materiel_id' : item['id'],        
      }
      try:
        # 反序列化数据
        schema = Stock_schema()
        # 验证数据
        stock_res = schema.load(stock_data)
      except ValidationError:
        return {'message': '库存数据验证失败'}, 422 # 422表单验证报错
      # 关联的库存表id
      stock_key = None
      # 库存表是否已有同类型库存
      exist = Stock.query.filter(Stock.materiel_id == stock_data['materiel_id']).first()
      if exist:
        stock_key = exist.id
        try:
          # 累加库存
          for key in stock_res: 
            if key in ['amount', 'gross']: setattr(exist, key, Decimal(stock_res[key])+getattr(exist, key))
          db.session.commit()
        except IntegrityError:
          return {'message': '更新库存失败'}, 421 # 421数据库操作报错
      else:
        try:
          stock_obj = Stock(**stock_res)
          db.session.add(stock_obj)
          db.session.commit()
          stock_key = stock_obj.id
        except IntegrityError:
          return {'message': '写入库存失败'}, 421 # 421数据库操作报错
      # <--- end
      # 写入进货表 --->
      try:
        batch_in_data = {
          'serial'     : request_data['serial'],
          'in_number'  : item['in_number'],
          'remainder'  : item['in_number'],
          'price'      : item['price'],
          'commission' : item['commission'] if item.__contains__('commission') else 0,
          'comment'    : item['comment'] if item.__contains__('comment') else '',
          'stock_id'   : stock_key,
        }
        # 反序列化数据
        schema = Batch_in_schema()
        # 验证数据
        Batch_in_res = schema.load(batch_in_data, partial=('commission', 'comment', 'stock_id'))
      except ValidationError:
        return {'message': '进货数据验证失败'}, 422 # 422表单验证报错
      try:
        db.session.add(Batch_in(**Batch_in_res))
        db.session.commit()
      except IntegrityError:
        # TODO: 回滚库存表操作
        return {'message': '写入进货数据失败'}, 421 # 421数据库操作报错
      # <--- end
    return {'message': '进货完成'}


restock_view = RestockAPI.as_view('restock_api')
restock_bp.add_url_rule('/list', view_func=restock_view, methods=['GET'])
restock_bp.add_url_rule('/create', view_func=restock_view, methods=['POST'])