from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.order import OrderModel
from schemas.order import OrderSchema
from libs.strings import gettext

order_schema = OrderSchema()
order_list_schema = OrderSchema(many=True)


class Order(Resource):
    @classmethod
    def get(cls, name: str):
        order = OrderModel.find_by_name(name)
        if order:
            return order_schema.dump(order), 200

        return {"message": gettext("order_not_found")}, 404


class OrderList(Resource):
    @classmethod
    def get(cls):
        return {"items": order_list_schema.dump(OrderModel.find_all())}, 200
