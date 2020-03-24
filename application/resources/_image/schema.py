from ...extensions import db, ma


class Image(db.Model):
    __tablename__ = "image"
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String, nullable=False)
    alt = db.Column(db.String, server_default="Image")


class ImageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Image

    uri = ma.auto_field(required=True)
    alt = ma.auto_field()
