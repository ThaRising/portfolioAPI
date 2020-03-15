from ...extensions import ma, db
from datetime import datetime
from ...shared import IMAGE_CATEGORY
from ...shared.validation import validate_uploads, validate_base64
from ...shared.exceptions import DataEncodingError
from ..image import Image, ImageSchema
from marshmallow import Schema, fields, validate


class PortfolioImage(db.Model):
    __tablename__ = "portfolio_image"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    preview_id = db.Column(db.Integer, db.ForeignKey(Image.id, use_alter=True))
    preview = db.relationship(Image, foreign_keys=[preview_id])
    images = db.relationship(Image, backref="portfolio_image", lazy=True, foreign_keys=[Image.parent_id])
    year = db.Column(db.Integer, default=datetime.today().year)
    client = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)


class PortfolioImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PortfolioImage

    content = ma.Nested(ImageSchema, many=True, attribute="images", dump_only=True)
    type = ma.String(default="image")
    preview = ma.Nested(ImageSchema)


class PostArgs(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    category = fields.Str(required=True, validate=lambda v: v in IMAGE_CATEGORY)
    preview = fields.Nested(ImageSchema, required=True)
    content = fields.List(fields.Nested(ImageSchema, required=True))
    year = fields.Int(validate=lambda v: len(str(v)) == 4)
    client = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str()
