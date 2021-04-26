from ma import ma
from models.payment import PaymentModel


class PaymentSchema(ma.ModelSchema):
    class Meta:
        model = PaymentModel
        dump_only = ("id", "amount", "payment_date", "paid_by", "order_id")
        include_fk = True