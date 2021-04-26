from flask_restful import Resource
from flask import send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os
from flask import jsonify, Response
import json
from libs import image_helper
from libs.strings import gettext
from schemas.address import AddressSchema
from models.address import AddressModel

address_schema = AddressSchema()


class Address(Resource):
    #@jwt_required
    @classmethod
    def get(self, address_id: int):
        """
        This endpoint returns the requested image if exists. It will use JWT to
        retrieve user information and look for the image inside the user's folder.
        """
        address = AddressModel.find_by_id(address_id)

        fulladdress = AddressModel.find_by_fulladdress()

        if not address:
            return {"message": gettext("user_not_found")}, 404

        return fulladdress, 200
        #return address_schema.dump(fulladdress), 200
