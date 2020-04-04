from flask_restplus import Namespace, Resource
from webargs.flaskparser import use_args, use_kwargs
from ...shared import QueryArgs
from .controller import ShopDigitalController
from .service import ShopDigitalService
from .schema import PostArgs, PatchArgs
from .._image.controller import ImageController
from flask_praetorian import roles_required
import requests
from flask import current_app
from ...shared.exceptions import InvalidPurchaseItem
import json

api = Namespace("shop")


@api.errorhandler(InvalidPurchaseItem)
def handle_ambiguous_type(error):
    return {'error': 'ERR_INVALID_PURCHASE_ITEM',
            'message': 'The provided item id does not correspond with a valid product.'}, 400


@api.route("/")
class ShopCollection(Resource):
    @use_args(QueryArgs(only=("fields",)), locations=("query",))
    def get(self, query: dict):
        result = ShopDigitalController().get({}, fields=query.get("fields"))
        return [] if not result else result

    @roles_required("admin")
    @use_args(QueryArgs(only=("fields",)), locations=("query",))
    @use_args(PostArgs, locations=("json",))
    def post(self, query, post):
        fields = query.get("fields")
        post_args = post
        preview = post_args.pop("preview")
        preview = ImageController().create({"uri": preview.get("uri"), "alt": preview.get("alt")})
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
        return [ShopDigitalController().update(kwargs.get("id_"), args[1], fields=args[0].get("fields"))]

    @roles_required("admin")
    def delete(self, id_):
        item_to_delete = ShopDigitalService().get({"id": id_})[0]
        ImageController().delete(item_to_delete.preview_id)
        [ImageController().delete(image.id) for image in item_to_delete.images]
        ShopDigitalController().delete(id_)


@api.route("/<string:id_>/payment")
class ShopItemPayment(Resource):
    base_url = "https://api.sandbox.paypal.com"

    def get(self, id_: str):
        item = ShopDigitalController().get({"id": id_}, fields=["current_price"])
        if not item or item is None:
            raise InvalidPurchaseItem
        headers = {
            'accept': "application/json",
            'accept-language': "de",
            'content-type': "application/x-www-form-urlencoded"
        }
        response = requests.post(f"{self.base_url}/v1/oauth2/token",
                                 data={"grant_type": "client_credentials"},
                                 auth=(current_app.config['CLIENT_ID'],
                                       current_app.config['CLIENT_SECRET']),
                                 headers=headers)
        access_token = response.json()["access_token"]
        payload = {
          "intent": "CAPTURE",
          "purchase_units": [
            {
              "reference_id": str(id_),
              "amount": {
                "currency_code": "EUR",
                "value": item.get("current_price")
              }
            }
          ],
          "application_context": {
            "return_url": "",
            "cancel_url": ""
          }
        }
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'accept-language': "de",
            'authorization': f"Bearer {access_token}"
        }
        response = requests.post(f"{self.base_url}/v2/checkout/orders",
                                 data=json.dumps(payload),
                                 headers=headers)
        return {
            "order_id": response.json()["id"]
        }, 201
