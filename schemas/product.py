
from ma import ma
from models.product import ProductModel


class ProductSchema(ma.ModelSchema):
    class Meta:
        model = ProductModel
        dump_only = ("id", "name", "description", "price", "image")
        include_fk = True


class ProductImageSchema(ma.ModelSchema):
    class Meta:
        model = ProductModel
        load_only = ("id", "name", "description", "price")
        dump_only = ("image")


