from ma import ma
from models.orderdetails import OrderDetailModel


class OrderDetailsSchema(ma.ModelSchema):
    class Meta:
        model = OrderDetailModel
        dump_only = ("id", "amount", "total_amount", "created_at", "order_id", "menu_id")
        include_fk = True
