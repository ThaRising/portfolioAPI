from flask_restplus import Resource, Namespace
from application.shared import QueryArgs
from webargs.flaskparser import use_kwargs, use_args
from .portfolio_controller import PortfolioController
from ..shared.exceptions import AmbiguousTypeError
from .portfolio_image.schema import PostArgs
import flask_praetorian

api = Namespace("portfolio")


@api.errorhandler(AmbiguousTypeError)
def handle_ambiguous_type(error):
    return {'error': 'ERR_AMBIGUOUS_TYPE',
            'message': 'Either a type value was not provided in the query string,'
                       ' or the type value is not "video" or "image".'}, 400


@api.errorhandler(flask_praetorian.PraetorianError)
def handle_auth_error(error):
    return {"error": "ERR_NOT_AUTHORIZED",
            "message": "Administrative privileges are required to use this endpoint."}, 401


@api.route("/")
class PortfolioImageCollection(Resource):
    @use_kwargs(QueryArgs(partial=("type",)), locations=("query",))
    def get(self, **kwargs):
        return PortfolioController().get_all(**kwargs)

    @flask_praetorian.roles_required('admin')
    @use_args(PostArgs, locations=("json",))
    @use_args(QueryArgs, locations=("query",))
    def post(self, post, query):
        return PortfolioController().create(query, post)


@api.route("/<string:id_>")
class PortfolioImageItem(Resource):
    @use_kwargs(QueryArgs, locations=("query",))
    def get(self, id_: str, **kwargs):
        return PortfolioController().get_one(id_, **kwargs)
