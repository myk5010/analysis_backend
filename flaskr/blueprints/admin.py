from flask import Blueprint, json ,jsonify
from flaskr.models import Materiel, Materiel_schema

# 资源路由
from flask.views import MethodView

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


class SettingApi(MethodView):
  
  def get(self, setting_id):
    if setting_id is None:
      list_data = Materiel.query.outerjoin('stocks').order_by(Materiel.id.desc()).all()
      # 序列化数据
      schema = Materiel_schema(many=True)
      return jsonify(schema.dump(list_data))
    else:
      pass


setting_view = SettingApi.as_view('setting_api')
admin_bp.add_url_rule('/system/', defaults={'setting_id': None}, view_func=setting_view, methods=['GET',])