from ...extensions import db, ma
from datetime import datetime


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.String, primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("shop_digital.id"), nullable=False)
    purchased_on = db.Column(db.DateTime, default=datetime.now)
    buyer_email = db.Column(db.String)
    uuid = db.Column(db.String)
    downloads_remaining = db.Column(db.Integer)


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        exclude = ("id", "uuid")

    product_id = ma.auto_field()
