from requests import Response
from db import db


class MenuImagesModel(db.Model):
    __tablename__ = "tblmenuimages"

    id = db.Column(db.Integer, primary_key=True)

    menu_id = db.Column(db.Integer, db.ForeignKey("tblmenu.id"), nullable=False)
    menu = db.relationship("MenuModel")

    image_id = db.Column(db.Integer, db.ForeignKey("tblmenuimage.id"), nullable=False)
    image = db.relationship("MenuImageModel")

    @classmethod
    def find_by_id(cls, _id: int) -> "MenuImagesModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
