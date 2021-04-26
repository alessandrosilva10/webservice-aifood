from typing import List
import datetime
from db import db


class PaymentModel(db.Model):
    __tablename__ = "tblpayments"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(12, 2), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    paid_by = db.Column(db.Integer, db.ForeignKey("tbluser.id"), nullable=False)
    user = db.relationship("UserModel")

    order_id = db.Column(db.Integer, db.ForeignKey("tblorders.id"), nullable=False)
    order = db.relationship("OrderModel")

    @classmethod
    def find_by_id(cls, paid_by: int) -> "PaymentModel":
        return cls.query.filter_by(paid_by=paid_by).first()

    @classmethod
    def find_all(cls) -> List["PaymentModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
