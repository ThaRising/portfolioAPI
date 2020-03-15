from ...extensions import db, ma


class Image(db.Model):
    __tablename__ = "image"
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("portfolio_image.id", use_alter=True), nullable=False)
    uri = db.Column(db.String, nullable=False)
    alt = db.Column(db.String, default="image")


class ImageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Image

    uri = ma.auto_field(required=True)
    alt = ma.auto_field()
