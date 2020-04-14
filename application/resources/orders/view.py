from flask_restplus import Namespace, Resource
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ..shop_digital.schema import ShopDigital
from flask import send_from_directory, current_app
from webargs.flaskparser import use_args
from ...shared import QueryArgs
from flask_praetorian import roles_required
from .controller import OrdersController
from .service import OrdersService
from ...shared.paypal import Paypal
from ...extensions import db
from werkzeug.utils import secure_filename
from ...shared.exceptions import PayPalTransactionError
from time import sleep

api = Namespace("orders")


@api.route("/")
class OrdersCollection(Resource):
    @roles_required('admin')
    @use_args(QueryArgs(only=("fields",)), locations=("query",))
    def get(self, query):
        orders = OrdersController().get({}, fields=query.get("fields"))
        if type(orders) == dict:
            if len(orders.keys()) < 1:
                return []
            return [orders]
        else:
            return orders


@api.route("/<string:id_>/")
class OrdersItem(Resource):
    def get(self, id_):
        order = Paypal(current_app.config["PAYPAL_URL"],
                       current_app.config["CLIENT_ID"],
                       current_app.config["CLIENT_SECRET"]).get_order(id_)
        if not order or order is None:
            raise PayPalTransactionError
        if order.json()["status"] != "COMPLETED":
            raise PayPalTransactionError
        s = Serializer(current_app.config["SECRET_KEY"], 6 * 60 * 60)
        uuid = s.dumps({'product_id': order.json()["purchase_units"][0]["reference_id"]}).decode('utf-8')
        sysorder = OrdersService().get({"id": id_})[0]
        if not sysorder or sysorder is None:
            raise PayPalTransactionError
        sysorder.uuid = uuid
        sysorder.buyer_email = order.json()["purchase_units"][0]["payee"]["email_address"]
        db.session.commit()
        return uuid


@api.route("/download/<string:uuid>/")
class Downloads(Resource):
    def get(self, uuid: str):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            product_id = s.loads(uuid)['product_id']
        except Exception:
            return "Invalid download key.", 400
        order = OrdersService().get({"uuid": uuid})[0]
        if order.downloads_remaining == 0:
            return "Maximum number of downloads have been reached.", 400
        elif order.downloads_remaining > 2:
            return "User download manipulation, download will not commence.", 400
        update = OrdersService().update(order.id, {"downloads_remaining": order.downloads_remaining - 1})
        product = ShopDigital.query.get(product_id)
        sleep(1)
        response = send_from_directory(directory=current_app.config["PRODUCT_DOWNLOADS"],
                                       filename=secure_filename(product.uri),
                                       mimetype="application/zip", as_attachment=True)
        response.cache_control.max_age = 0
        response.cache_control.public = True
        response.headers['Cache-Control'] = 'no-store'
        return response
