from typing import List

from db import db


class OrderItemModel(db.Model):
    __tablename__ = "order_items"
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("UserModel")

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    order = db.relationship("OrderModel")

    @classmethod
    def find_by_name(cls, name: str) -> "OrderItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["OrderItemModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
