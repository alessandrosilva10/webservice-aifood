from flask_restful import Resource
from flask import request
from datetime import datetime
from datetime import timedelta
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from flask_bcrypt import Bcrypt
import traceback
from models.user import UserModel
from schemas.user import UserSchema
from models.confirmation import ConfirmationModel
from blacklist import BLACKLIST
from libs.mailgun import MailGunException
from libs.strings import gettext, generate_string

user_schema = UserSchema()

bcrypt = Bcrypt()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            print('oi')
            return {"message": gettext("user_username_exists")}, 400

        if UserModel.find_by_email(user.email):
            return {"message": gettext("user_email_exists")}, 400

        try:
            pw_hash = bcrypt.generate_password_hash(user.password, 10).decode('utf-8')

            user.password = pw_hash

            user.save_to_db()

            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            # user.send_confirmation_email()
            return {"message": gettext("user_registered")}, 201
        except MailGunException as e:
            user.delete_from_db()  # rollback
            return {"message": str(e)}, 500
        except:  # failed to save user to db
            traceback.print_exc()
            user.delete_from_db()  # rollback
            return {"message": gettext("user_error_creating")}, 500


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        user.delete_from_db()
        return {"message": gettext("user_deleted")}, 200


class GetUserInfo(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    @jwt_required
    def post(cls):
        user_json = request.get_json()
        current_user = get_jwt_identity()

        if user_json["id"] == current_user:
            if UserModel.find_by_id(user_json["id"]):
                user = UserModel.find_by_id(user_json["id"])
                return user_schema.dump(user), 200
            else:
                return {"message": "User not found"}, 400
        else:
            return "Unauthorized", 401

    @classmethod
    # @jwt_required
    def get(cls):
        users = UserModel.find_all()

        return user_schema.dump(users), 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",))
        user = UserModel.find_by_username(user_data.username)

        # if user and safe_str_cmp(user.password, user_data.password):
        if user and bcrypt.check_password_hash(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(user.id, expires_delta=timedelta(seconds=86400), fresh=True)
                refresh_token = create_refresh_token(user.id, expires_delta=timedelta(seconds=86400))
                return (
                    {"access_token": access_token, "refresh_token": refresh_token},
                    200,
                )
            return {"message": gettext("user_not_confirmed").format(user.email)}, 400

        return {"message": gettext("user_invalid_credentials")}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
