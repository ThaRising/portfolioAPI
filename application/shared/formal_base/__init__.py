from abc import ABC, abstractmethod
from typing import Optional, List
from ...extensions import db


class Component(ABC):
    @abstractmethod
    def get(self, params: dict, **kwargs) -> Optional[List[db.Model]]: pass

    @abstractmethod
    def create(self, params: dict, **kwargs) -> db.Model: pass

    @abstractmethod
    def update(self, key: int, params: dict, **kwargs) -> Optional[db.Model]: pass

    @abstractmethod
    def delete(self, key: int) -> None: pass


__all__ = []
