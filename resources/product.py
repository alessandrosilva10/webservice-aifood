from flask_restful import Resource
from flask import request
import simplejson

from models.product import ProductModel
from schemas.product import ProductSchema, ProductImageSchema
from libs.strings import gettext

product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)
product_image_list_schema = ProductImageSchema(many=True)

class Product(Resource):
    @classmethod
    def get(cls, name: str):
        order = OrderModel.find_by_name(name)
        if order:
            return order_schema.dump(order), 200

        return {"message": gettext("order_not_found")}, 404


class ProductList(Resource):
    @classmethod
    def get(cls):
        return {"products": product_list_schema.dump(ProductModel.find_all())}, 200


class ProductImageList(Resource):
    @classmethod
    def get(cls):
        return {"images": product_image_list_schema.dump(ProductModel.find_all_images())}, 200