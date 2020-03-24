from ...shared import Controller
from .service import ShopDigitalService
from .schema import ShopDigitalSchema
from ...extensions import db
from ...shared.exceptions import AmbiguousFieldError


class ShopDigitalController(Controller):
    def __init__(self):
        super(ShopDigitalController, self).__init__(ShopDigitalService, ShopDigitalSchema)

    def create(self, params: dict, **kwargs) -> db.Model:
        fields: list = kwargs.get("fields")
        try:
            schema = self.schema(only=(*fields,) if fields else None)
        except ValueError:
            raise AmbiguousFieldError
        content: list = kwargs.get("content")
        preview: object = kwargs.get("preview")
        created_item = self.service().create(params)
        created_item.images.extend(content)
        created_item.preview = preview
        db.session.commit()
        return schema.dump(created_item)
