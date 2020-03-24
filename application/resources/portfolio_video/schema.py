from ...extensions import ma, db
from datetime import datetime
from marshmallow import post_dump
from .._image import Image, ImageSchema


class PortfolioVideo(db.Model):
    __tablename__ = "portfolio_video"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    preview_id = db.Column(db.Integer, db.ForeignKey(Image.id, use_alter=True))
    preview = db.relationship(Image, foreign_keys=[preview_id])
    video = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, default=datetime.today().year)
    client = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)


class PortfolioVideoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PortfolioVideo

    type = ma.String(default="video")
    content = ma.String(attribute="video", dump_only=True)
    preview = ma.Nested(ImageSchema, data_key="preview")

    @post_dump
    def change(self, data, many):
        if "video" in data:
            data.pop("video")
        return data
