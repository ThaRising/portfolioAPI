from ...shared import Controller
from .service import PortfolioVideoService
from .schema import PortfolioVideoSchema
from ...extensions import db
from ...shared.exceptions import AmbiguousFieldError
from re import search


class PortfolioVideoController(Controller):
    def __init__(self):
        super(PortfolioVideoController, self).__init__(PortfolioVideoService, PortfolioVideoSchema)

    def create(self, params: dict, **kwargs) -> db.Model:
        fields: list = kwargs.get("fields")
        try:
            schema = self.schema(only=(*fields,) if fields else None)
        except ValueError:
            raise AmbiguousFieldError
        params["video"] = search("v=[^&]*", params.pop("content")).group()[2:]
        preview: object = kwargs.get("preview")
        created_item = self.service().create(params)
        created_item.preview = preview
        db.session.commit()
        return schema.dump(created_item)
