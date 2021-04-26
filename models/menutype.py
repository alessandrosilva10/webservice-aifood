from requests import Response
from db import db


class MenuTypeModel(db.Model):
    __tablename__ = "tblmenutype"

    id = db.Column(db.Integer, primary_key=True)
    menu_type = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)

    @classmethod
    def find_by_menutype(cls, menu_type: str) -> "MenuTypeModel":
        return cls.query.filter_by(menu_type=menu_type).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "MenuTypeModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()



