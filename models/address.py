from requests import Response
from db import db
from models.user import UserModel
import json
from flask import jsonify, make_response


class AddressModel(db.Model):
    __tablename__ = "tbladdress"

    id = db.Column(db.Integer, primary_key=True)
    user_first_name = db.Column(db.String(80), nullable=False)
    user_last_name = db.Column(db.String(80), nullable=False)
    user_phone_number = db.Column(db.String(14), nullable=False, unique=True)
    user_landline = db.Column(db.String(14), nullable=False, unique=True)
    user_image_path = db.Column(db.String(50), nullable=False, unique=True)
    account_status = db.Column(db.Boolean(), default=True)

    user_id = db.Column(db.Integer, db.ForeignKey("tbluser.id"), nullable=False)
    user = db.relationship("UserModel")

    @classmethod
    def find_by_fulladdress(cls):
        # return db.session.query(AddressModel).join(UserModel, AddressModel.user_id == UserModel.id).all()

        CONST_TABLES = {"tbluser": "public.tbluser", "tbladdress": "public.tbladdress"}
        CONST_SELECT = {"user_first_name": "user_first_name", "user_last_name": "user_last_name",
                        "user_phone_number": "user_phone_number", "user_landline": "user_landline",
                        "user_image_path": "user_image_path", "username": "username",
                        "email": "email", "account_status": "account_status", "is_admin": "isAdmin"}

        result = db.session.execute(""
                                    "SELECT {}, {}, {}, {}, "
                                    "{}, {}, {}, {}, {}"
                                    " FROM {} AS C INNER JOIN {} AS F ON C.user_id = F.id".
                                    format(CONST_SELECT["user_first_name"], CONST_SELECT["user_last_name"],
                                           CONST_SELECT["user_phone_number"], CONST_SELECT["user_landline"],
                                           CONST_SELECT["user_image_path"], CONST_SELECT["username"],
                                           CONST_SELECT["email"], CONST_SELECT["account_status"], CONST_SELECT["is_admin"],
                                           CONST_TABLES["tbladdress"], CONST_TABLES["tbluser"]
                                           )
                                    )

        # If no rows were returned in the result, return an empty list
        if not result.returns_rows:
            response = []

        # Convert the response to a plain list of dicts
        else:
            response = [dict(row.items()) for row in result]

        return response

    @classmethod
    def find_by_firstname(cls, user_first_name: str) -> "AddressModel":
        return cls.query.filter_by(user_first_name=user_first_name).first()

    @classmethod
    def find_by_phone_number(cls, user_phone_number: str) -> "AddressModel":
        return cls.query.filter_by(user_phone_number=user_phone_number).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "AddressModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
