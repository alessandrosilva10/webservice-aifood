from requests import Response
from db import db


class VoucherUserModel(db.Model):
    __tablename__ = "tblvoucheruser"

    id = db.Column(db.Integer, primary_key=True)
    voucher_id = db.Column(db.Integer, db.ForeignKey("tblvoucher.id"), nullable=False)
    voucher = db.relationship("VoucherModel")

    user_id = db.Column(db.Integer, db.ForeignKey("tbluser.id"), nullable=False)
    user = db.relationship("UserModal")

    @classmethod
    def find_by_voucherid(cls, voucher_id: str) -> "VoucherUserModel":
        return cls.query.filter_by(voucher_id=voucher_id).first()

    @classmethod
    def find_by_userid(cls, user_id: str) -> "VoucherUserModel":
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
