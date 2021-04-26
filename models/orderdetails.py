from typing import List

from db import db


class OrderDetailModel(db.Model):
    __tablename__ = "tblorderdetails"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(12, 2), nullable=False)
    total_amount = db.Column(db.Float(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    order_id = db.Column(db.Integer, db.ForeignKey("tblorders.id"), nullable=False)
    order = db.relationship("OrderModel", lazy="dynamic", cascade="all, delete-orphan")

    menu_id = db.Column(db.Integer, db.ForeignKey("tblmenu.id"), nullable=False)
    menu = db.relationship("MenuModel", lazy="dynamic", cascade="all, delete-orphan")

    @classmethod
    def find_by_user_id(cls, user_id: integer) -> "OrderDetailModel":
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_all(cls) -> List["OrderDetailModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
