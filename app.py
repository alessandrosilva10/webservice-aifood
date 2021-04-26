from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from flask_uploads import configure_uploads, patch_request_class
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from db import db
from ma import ma
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout, GetUserInfo
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.order import Order, OrderList
from resources.product import ProductList, ProductImageList
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.image import ImageUpload, Image, AvatarUpload, Avatar
from resources.address import Address
from resources.payment import Payment

from libs.image_helper import IMAGE_SET
from flask_migrate import Migrate
from flask_socketio import SocketIO, send, emit
import stripe
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")  # load default configs from default_config.py
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)

stripe.api_key = os.environ.get("SK_TEST_KEY")

patch_request_class(app, 10 * 1024 * 1024)  # restrict max upload image size to 10MB
configure_uploads(app, IMAGE_SET)
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=10, ping_interval=5)
db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


# https://www.tecmint.com/install-postgresql-and-pgadmin-in-ubuntu/
# https://stackoverflow.com/questions/17711324/database-structure-for-customer-table-having-many-orders-per-customer-and-many/17711375
# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(GetUserInfo, "/users")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:user_id>")
api.add_resource(Order, "/order")

api.add_resource(Address, "/address/<int:address_id>")
api.add_resource(ProductList, "/products")
api.add_resource(ProductImageList, "/products_images")

from random import random
import time
from models.item import ItemModel
from schemas.item import ItemSchema

item_list_schema = ItemSchema(many=True)


@socketio.on('test_message')  # Decorator to catch an event called "my event":
def test_message(message):  # test_message() is the event callback function.
    strapi_token = message["data"]
    print(strapi_token)
    if strapi_token != "teste":
        resp = stripe.Charge.create(
            amount=5000, #content['amount']
            currency="brl",
            source=strapi_token,
            #receipt_email=content['receiptEmail'],
        )

        emit('test_message', {'data': resp})

    #a = item_list_schema.dump(ItemModel.find_all())
    #print(a)



@app.route('/items', methods=['GET'])
def get():
    test_message('test_message')


if __name__ == "__main__":
    # app.run(port=5000, debug=True)
    socketio.run(app, port=5000, host='0.0.0.0')
