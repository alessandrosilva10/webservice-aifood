from requests import Response
from db import db


class MenuModel(db.Model):
    __tablename__ = "tblmenu"

    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(12, 2), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    additional = db.Column(db.String(500), nullable=True)
    menu_status = db.Column(db.Boolean(), default=True)

    menu_id = db.Column(db.Integer, db.ForeignKey("tblmenutype.id"), nullable=False)
    menu = db.relationship("MenuTypeModel")

    @classmethod
    def find_by_menuname(cls, menuname: str) -> "MenuModel":
        return cls.query.filter_by(menuname=menuname).first()

    @classmethod
    def find_by_price(cls, price: float) -> "MenuModel":
        return cls.query.filter_by(price=price).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "MenuModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
