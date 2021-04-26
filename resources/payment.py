from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.payment import PaymentModel
from schemas.payment import PaymentSchema
from libs.strings import gettext

payment_schema = PaymentSchema()
payment_list_schema = PaymentSchema(many=True)


class Payment(Resource):
    @classmethod
    @jwt_required
    def get(cls, id: int):
        payment = PaymentModel.find_by_id(id)
        if order:
            return payment_schema.dump(payment), 200

        return {"message": gettext("order_not_found")}, 404


class PaymentList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {"items": order_list_schema.dump(OrderModel.find_all())}, 200
