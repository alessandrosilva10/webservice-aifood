from ma import ma
from models.menu import MenuModel


class MenuSchema(ma.ModelSchema):
    class Meta:
        model = MenuModel
        load_only = ("menu",)
        dump_only = ("id", "menu_name", "price", "ingredients", "additional", "menu_status", "account_status")
        include_fk = True