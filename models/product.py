from typing import List
from sqlalchemy.orm import defer, undefer_group
from db import db


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.DECIMAL(asdecimal=False),nullable=False)
    image = db.Column(db.String(100), nullable=False)
    #image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)
    #image = db.relationship("ImageModel")

    @classmethod
    def find_by_name(cls, name: str) -> "ProductModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["ProductModel"]:
        return cls.query.all()

    @classmethod
    def find_all_images(cls) -> List["ProductModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
