from ...shared import Service
from .schema import ShopDigital


class ShopDigitalService(Service):
    def __init__(self):
        super(ShopDigitalService, self).__init__(ShopDigital)
