from flask_restplus import Resource, Namespace
from application.shared import QueryArgs
from webargs.flaskparser import use_kwargs, use_args
from .portfolio_image.schema import PostArgs, VideoPostArgs
import flask_praetorian
from collections import namedtuple
from .portfolio_image import PortfolioImageController
from .portfolio_image.service import PortfolioImageService
from .portfolio_video import PortfolioVideoController
from .portfolio_video.service import PortfolioVideoService
from ._image.controller import ImageController

api = Namespace("portfolio")


@api.route("/")
class PortfolioCollection(Resource):
    @use_args(QueryArgs(partial=("type",)), locations=("query",))
    def get(self, query: dict):
        QueryParameters = namedtuple("QueryParameters",
                                     "fields, type")
        query_args = QueryParameters(query.get("fields"), query.get("type"))

        if not query_args.type:
            output = [PortfolioImageController().get({}, fields=query_args.fields),
                      PortfolioVideoController().get({}, fields=query_args.fields)]
            for i, j in enumerate(output):
                if type(j) != list:
                    output[i] = [j]
            return [item for sublist in output for item in sublist if item]

        elif query_args.type == "image":
            return PortfolioImageController().get({}, fields=query_args.fields)

        elif query_args.type == "video":
            return PortfolioVideoController().get({}, fields=query_args.fields)

    @flask_praetorian.roles_required('admin')
    @use_args(QueryArgs, locations=("query",))
    def post(self, query):
        QueryParameters = namedtuple("QueryParameters",
                                     "fields, type")
        query_args = QueryParameters(query.get("fields"), query.get("type"))

        @use_args(PostArgs, locations=("json",))
        def post_image(post):
            post_args = post
            preview = post_args.pop("preview")
            preview = ImageController().create({"uri": preview.get("uri"),
                                                "alt": preview.get("alt")}, preview=True)

            content = post_args.pop("content")
            content = [ImageController().create({"uri": i.get("uri"), "alt": i.get("alt")}) for i in content]
            return \
                PortfolioImageController().create(post_args, fields=query_args.fields, content=content, preview=preview)

        @use_args(VideoPostArgs, locations=("json",))
        def post_video(post):
            post_args = post
            preview = post_args.pop("preview")
            preview = ImageController().create({"uri": preview.get("uri"),
                                                "alt": preview.get("alt")}, preview=True)

            return PortfolioVideoController().create(post_args, fields=query_args.fields, preview=preview)

        if query_args.type == "image":
            fn = post_image()
        else:
            fn = post_video()
        return fn


@api.route("/<string:id_>")
class PortfolioItem(Resource):
    @use_kwargs(QueryArgs, locations=("query",))
    def get(self, id_: str, **kwargs):
        QueryParameters = namedtuple("QueryParameters",
                                     "fields, type")
        query_args = QueryParameters(kwargs.get("fields"), kwargs.get("type"))

        if query_args.type == "image":
            return PortfolioImageController().get({"id": id_}, fields=query_args.fields)

        elif query_args.type == "video":
            return PortfolioVideoController().get({"id": id_}, fields=query_args.fields)

    @flask_praetorian.roles_required('admin')
    @use_kwargs(PostArgs(
        only=("title", "category", "year", "client", "description"),
        partial=("title", "category", "client")),
        locations=("json",))
    @use_kwargs(QueryArgs, locations=("query",))
    def patch(self, id_: str, **kwargs):
        QueryParameters = namedtuple("QueryParameters",
                                     "fields, type")
        query_args = QueryParameters(kwargs.pop("fields", None), kwargs.pop("type"))

        if query_args.type == "image":
            return PortfolioImageController().update(id_, kwargs, fields=query_args.fields)

        elif query_args.type == "video":
            return PortfolioVideoController().update(id_, kwargs, fields=query_args.fields)

    @flask_praetorian.roles_required('admin')
    @use_kwargs(QueryArgs(only=("type",)), locations=("query",))
    def delete(self, id_: str, **kwargs):
        type_ = kwargs.get("type")
        if type_ == "image":
            item_to_delete = PortfolioImageService().get({"id": id_})[0]
            ImageController().delete(item_to_delete.preview_id)
            [ImageController().delete(image.id) for image in item_to_delete.images]
            PortfolioImageController().delete(id_)

        elif type_ == "video":
            item_to_delete = PortfolioVideoService().get({"id": id_})[0]
            ImageController().delete(item_to_delete.preview_id)
            PortfolioVideoController().delete(id_)
