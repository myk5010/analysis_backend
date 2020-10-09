from flask import Blueprint, json, jsonify, request
from flaskr import db

# 资源路由
from flask.views import MethodView

outstock_bp = Blueprint('outstock', __name__, url_prefix='/outstock')


class OutstockAPI(MethodView):

  def get(self):
    dict_request = request.values.to_dict()
    pass


  def post(self):
    return '222'


outstock_view = OutstockAPI.as_view('outstock_api')
outstock_bp.add_url_rule('', view_func=outstock_view, methods=['GET'])
outstock_bp.add_url_rule('', view_func=outstock_view, methods=['POST'])