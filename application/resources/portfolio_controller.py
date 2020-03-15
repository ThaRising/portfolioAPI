from .portfolio_image.schema import PortfolioImageSchema
from .portfolio_image.service import PortfolioImageService
from .portfolio_video.schema import PortfolioVideoSchema
from .portfolio_video.service import PortfolioVideoService
from .image import ImageService
import base64
from datetime import datetime
import random
import string
from werkzeug.utils import secure_filename
from collections import namedtuple


class PortfolioController:
    def __init__(self):
        self.schema_image = PortfolioImageSchema
        self.schema_video = PortfolioVideoSchema
        self.service_image = PortfolioImageService
        self.service_video = PortfolioVideoService

    def __validate_type(self, type_):
        if type_ == "image":
            service = self.service_image
            schema = self.schema_image
            return service, schema
        elif type_ == "video":
            service = self.service_video
            schema = self.schema_video
            return service, schema

    def __upload_image(self, image):
        imgdata = base64.b64decode(image.get("uri"))
        random_chars = (lambda r: "".join([random.choice(string.ascii_letters) for i in range(r)]))
        filename = secure_filename(f"{datetime.now()}{random_chars(5)}")
        with open(filename, 'wb') as f:
            f.write(imgdata)
        return filename, image.get("alt")

    def get_all(self, **kwargs):
        """
        :param kwargs: Parsed query arguments for filtering the function output
        :return: All portfolio items (includes portfolio_image and portfolio_video)
        """
        QueryParameters = namedtuple("QueryParameters",
                                     "fields, type")
        params = QueryParameters(kwargs.get("fields"), kwargs.get("type"))

        filter_image = self.schema_image(many=True)
        filter_video = self.schema_video(many=True)
        flatten = (lambda l: [item for sublist in l for item in sublist])

        if params.fields and params.fields is not None and not params.fields[0] == "":
            filter_image = self.schema_image(many=True, only=(*params.fields,))
            filter_video = self.schema_video(many=True, only=(*params.fields,))

        if params.type == "image":
            output = filter_image.dump(self.service_image().get({}))
            flatten = None
        elif params.type == "video":
            output = filter_video.dump(self.service_video().get({}))
            flatten = None
        else:
            output = [filter_image.dump(self.service_image().get({})),
                      filter_video.dump(self.service_video().get({}))]

        return flatten(output) if flatten else output

    def get_one(self, id_, **kwargs):
        """
        :param id_: Database ID of the item to retrieve
        :param kwargs: Parsed query arguments for filtering the function output
        :return: Either a portfolio_image or a portfolio_video by id
        """
        QueryParameters = namedtuple("QueryParameters",
                                     "fields, type")
        params = QueryParameters(kwargs.get("fields"), kwargs.get("type"))
        service, schema = self.__validate_type(params.type)
        if params.fields and params.fields is not None and not params.fields[0] == "":
            return schema(many=True, only=(*params.fields,)).dump(service().get({"id": id_}))
        else:
            return schema(many=True).dump(service().get({"id": id_}))

    def create(self, query, params: dict):
        """
        :param query: Parsed query arguments for filtering the function output
        :param params: Parsed JSON arguments for creating the database row
        :return: The created portfolio_image or portfolio_video serialized according to the respective schema
        """
        QueryParameters = namedtuple("QueryParameters",
                                     "fields, type")
        Parameters = namedtuple("Parameters",
                                "preview, content, remainder")

        query_params = QueryParameters(query.get("fields"), query.get("type"))
        json_params = Parameters(params.pop("preview"), params.pop("content"), params)

        service, schema = self.__validate_type(query.get("type"))
        images = params.pop("content")
        item = service().create(params)
        preview = params.pop("preview")
        if type(preview) != int:
            filename, alt = self.__upload_image(preview)
            ImageService().create({"parent_id": 0, "uri": filename, "alt": alt})
        else:
            item.preview_id = preview
        images = [self.__upload_image(image) for image in images]
        [ImageService().create({"parent_id": item.id, "uri": f, "alt": a}) for f, a in images]
        # Create field mask and serialize data
        fields = query.get("fields")
        if fields and fields is not None and not fields[0] == "":
            return schema(only=(*fields,)).dump(item)
        else:
            return schema().dump(item)
