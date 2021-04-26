from ma import ma
from models.user import UserModel


class OrderSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("user",)
        dump_only = ("id",)
        include_fk = True
