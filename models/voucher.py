from requests import Response
from db import db


class VoucherModel(db.Model):
    __tablename__ = "tblvoucher"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(80), nullable=False)
    valid_until = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean(), default=False)

    @classmethod
    def find_by_name(cls, name: str) -> "VoucherModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_active(cls, active: str) -> "VoucherModel":
        return cls.query.filter_by(active=active).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "VoucherModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
