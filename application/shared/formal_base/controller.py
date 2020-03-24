from . import Component
from .service import Service
from typing import Optional, Type
from ...extensions import db
from ..exceptions import AmbiguousFieldError


class Controller(Component):
    def __init__(self,
                 service: Type[Service],
                 schema: any):
        self.service = service
        self.schema = schema

    def get(self, params: dict, **kwargs) -> dict:
        output: list = self.service().get(params)
        if not output:
            return {}
        output = output if len(output) > 1 else output[0]
        fields: list = kwargs.get("fields")
        args = {"many": True if type(output) == list else False,
                "only": (*fields,) if fields else None}
        try:
            schema = self.schema(**args)
        except ValueError:
            raise AmbiguousFieldError
        return schema.dump(output)

    def create(self, params: dict, **kwargs) -> db.Model:
        output: list = self.service().create(params)
        fields: list = kwargs.get("fields")
        try:
            schema = self.schema(only=(*fields,) if fields else None)
        except ValueError:
            return schema.dump(output)
        return schema.dump(output)

    def update(self, key: int, params: dict, **kwargs) -> Optional[db.Model]:
        output: list = self.service().update(key, params)
        fields: list = kwargs.get("fields")
        try:
            schema = self.schema(only=(*fields,) if fields else None)
        except ValueError:
            raise AmbiguousFieldError
        return schema.dump(output)

    def delete(self, key: int) -> None:
        self.service().delete(key)
