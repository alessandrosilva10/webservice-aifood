from ma import ma
from models.address import AddressModel


class AddressSchema(ma.ModelSchema):
    class Meta:
        model = AddressModel
        load_only = ("user",)
        dump_only = ("id", "user_first_name", "user_last_name", "user_phone_number", "user_landline", "user_image_path", "account_status")
        include_fk = True


        """SELECT *
FROM public.tbladdress AS C 
INNER JOIN public.tbluser AS F ON C.user_id = F.id"""