from ...extensions import db, ma
from .._image import Image, ImageSchema
from marshmallow import Schema, fields, validate


class ShopDigital(db.Model):
    __tablename__ = "shop_digital"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    preview_id = db.Column(db.Integer, db.ForeignKey(Image.id, use_alter=True))
    preview = db.relationship(Image, foreign_keys=[preview_id])
    images = db.relationship(Image, secondary="shop_association")
    base_price = db.Column(db.Float, nullable=False)
    sale = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    uri = db.Column(db.String, nullable=False)


shop_assoc = db.Table("shop_association",
                      db.Column("id", db.Integer, primary_key=True),
                      db.Column("image", db.Integer, db.ForeignKey(Image.id)),
                      db.Column("item", db.Integer, db.ForeignKey(ShopDigital.id)))


class ShopDigitalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ShopDigital
        exclude = ("uri",)

    content = ma.Nested(ImageSchema, attribute="images", many=True, required=True)
    preview = ma.Nested(ImageSchema, required=True)
    type = ma.String(default="digital", dump_only=True)
    current_price = ma.Method("calc_current_price", dump_only=True)

    def calc_current_price(self, obj) -> float:
        if not obj.sale:
            return f"{obj.base_price:.2f}"
        return "{0:.2f}".format(obj.base_price - (obj.base_price * (obj.sale / 100)))


class PostArgs(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    content = fields.List(fields.Nested(ImageSchema, required=True))
    preview = fields.Nested(ImageSchema, required=True)
    base_price = fields.Float(required=True, validate=lambda v: v >= 0.01)
    description = fields.Str()


class PatchArgs(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=50))
    base_price = fields.Float(required=True, validate=lambda v: v >= 0.01)
    description = fields.Str()
    sale = fields.Int(validate=validate.Range(min=1, max=99))
