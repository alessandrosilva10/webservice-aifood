from ma import ma
from models.menuimages import MenuImagesModel


class MenuImagesSchema(ma.ModelSchema):
    class Meta:
        model = MenuImagesModel
        dump_only = ("id", "menu_id", "image_id")
        include_fk = True