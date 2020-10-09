from flask import Blueprint, json, jsonify, request
from flaskr import db
from sqlalchemy.exc import IntegrityError
from flaskr.models import materiel
from marshmallow import ValidationError

# 资源路由
from flask.views import MethodView

admin_bp = Blueprint('setting', __name__, url_prefix='/setting')


class SettingAPI(MethodView):
  
  def get(self):
    dict_request = request.values.to_dict()
    # 序列化数据
    schema = materiel.Materiel_schema(many=True, exclude=['stocks'])
    # sql语句
    sql = materiel.Materiel.query.order_by(materiel.Materiel.id.desc())
    # 筛选
    if dict_request.__contains__('materiel_name'):  sql = sql.filter(materiel.Materiel.materiel_name.like('%'+dict_request['materiel_name']+'%')) 
    if dict_request.__contains__('standard'):       sql = sql.filter(materiel.Materiel.standard.like('%'+dict_request['standard']+'%')) 
    if dict_request.__contains__('unit'):           sql = sql.filter(materiel.Materiel.unit.like('%'+dict_request['unit']+'%')) 
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
    request_data = request.json
    try:
      # 反序列化数据
      schema = materiel.Materiel_schema()
      # 验证数据
      res = schema.load(request_data)
    except ValidationError:
      # 422错误状态码, 表单验证错误专用
      return {'message': ValidationError.messages}, 422
    try:
      db.session.add(materiel.Materiel(**res))
      db.session.commit()
    except IntegrityError:
      # print(IntegrityError)
      # db.session.rollback()
      return {'message': '物料名称不能重复,提交失败'}, 421 # 421数据库报错
    else:
      return {'message': '提交成功'}


setting_view = SettingAPI.as_view('setting_api')
admin_bp.add_url_rule('/category', view_func=setting_view, methods=['GET'])
admin_bp.add_url_rule('/category', view_func=setting_view, methods=['POST'])