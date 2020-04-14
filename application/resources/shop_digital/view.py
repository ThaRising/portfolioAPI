from flask_restplus import Namespace, Resource
from webargs.flaskparser import use_args
from ...shared import QueryArgs
from .controller import ShopDigitalController
from .service import ShopDigitalService
from .schema import PatchArgs
from .._image.controller import ImageController
from flask_praetorian import roles_required
from ...shared.exceptions import InvalidPurchaseItem
from ...shared.paypal import Paypal
from flask import current_app, request
from werkzeug.utils import secure_filename
from ..orders.controller import OrdersController
from ast import literal_eval
from pathlib import Path

api = Namespace("shop")


@api.route("/")
class ShopCollection(Resource):
    @use_args(QueryArgs(only=("fields",)), locations=("query",))
    def get(self, query: dict):
        result = ShopDigitalController().get({}, fields=query.get("fields"))
        return [] if not result else result

    @roles_required("admin")
    @use_args(QueryArgs(only=("fields",)), locations=("query",))
    def post(self, query):
        post_args: dict = literal_eval(request.form.get("data"))
        file = request.files["file"]
        filename = secure_filename(file.filename)
        post_args["uri"] = filename
        file.save(Path(current_app.config["PRODUCT_DOWNLOADS"]) / filename)
        fields = query.get("fields")
        preview = post_args.pop("preview")
        preview = ImageController().create({"uri": preview.get("uri"),
                                            "alt": preview.get("alt")}, preview=True)
        content = post_args.pop("content")
        content = [ImageController().create({"uri": i.get("uri"), "alt": i.get("alt")}) for i in content]
        return ShopDigitalController().create(post_args, fields=fields, content=content, preview=preview)


@api.route("/<string:id_>")
class ShopItem(Resource):
    @use_args(QueryArgs(only=("fields",)), locations=("query",))
    def get(self, *args, **kwargs):
        return [ShopDigitalController().get({"id": kwargs.get("id_")}, fields=args[0].get("fields"))]

    @roles_required("admin")
    @use_args(QueryArgs(only=("fields",)), locations=("query",))
    @use_args(PatchArgs, locations=("json",))
    def patch(self, *args, **kwargs):
        return ShopDigitalController().update(kwargs.get("id_"), args[1], fields=args[0].get("fields"))

    @roles_required("admin")
    def delete(self, id_):
        item_to_delete = ShopDigitalService().get({"id": id_})[0]
        ImageController().delete(item_to_delete.preview_id)
        [ImageController().delete(image.id) for image in item_to_delete.images]
        Path.unlink(current_app.config["PRODUCT_DOWNLOADS"] / item_to_delete.uri)
        ShopDigitalController().delete(id_)


@api.route("/<string:id_>/payment/")
class ShopItemPayment(Resource):
    def get(self, id_: str):
        item = ShopDigitalController().get({"id": id_}, fields=["current_price"])
        if not item or item is None:
            raise InvalidPurchaseItem
        response = Paypal(current_app.config["PAYPAL_URL"],
                          current_app.config["CLIENT_ID"],
                          current_app.config["CLIENT_SECRET"]).create_payment(id_, item)
        order_id = response.json()["id"]
        OrdersController().create({"id": order_id,
                                   "product_id": id_,
                                   "downloads_remaining": 2})
        return {
            "order_id": order_id
        }, 201
