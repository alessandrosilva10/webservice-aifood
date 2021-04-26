from models.menuimage import MenuImageModel


class MenuImageSchema(ma.ModelSchema):
    class Meta:
        model = MenuImageModel
        dump_only = ("id", "path")

