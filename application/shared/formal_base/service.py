from . import Component
from ...extensions import db
from typing import Optional, List
from ..exceptions import DataIntegrityError
from sqlalchemy import exc


class Service(Component):
    def __init__(self, model: db.Model) -> None:
        self.model: db.Model = model

    def get(self, params: dict, **kwargs) -> Optional[List[db.Model]]:
        return self.model.query.filter_by(**params).all()

    def create(self, params: dict, **kwargs) -> db.Model:
        try:
            created_object = self.model(**params)
            db.session.add(created_object)
            db.session.commit()
        except exc.IntegrityError or ValueError:
            db.session.rollback()
            raise DataIntegrityError
        return created_object

    def update(self, key: int, params: dict, **kwargs) -> Optional[db.Model]:
        update_model = self.model.query.filter_by(id=key)
        if not update_model or update_model is None:
            raise exc.AmbiguousForeignKeysError
        update_model.update(params)
        db.session.commit()
        return update_model.first()

    def delete(self, key: int) -> None:
        delete_model = self.model.query.get(key)
        if not delete_model or delete_model is None:
            raise exc.AmbiguousForeignKeysError
        db.session.delete(delete_model)
        db.session.commit()
