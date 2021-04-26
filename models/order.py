from typing import List
import datetime
from db import db


class OrderModel(db.Model):
    __tablename__ = "tblorders"

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    total_amount = db.Column(db.Float(12, 2), nullable=False)
    order_status = db.Column(db.Boolean(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("tbluser.id"), nullable=False)
    user = db.relationship("UserModel")

    @classmethod
    def find_by_user_id(cls, user_id: int) -> "OrderModel":
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
