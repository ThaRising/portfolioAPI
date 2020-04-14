from ...shared import Controller
from .service import OrdersService
from .schema import OrderSchema


class OrdersController(Controller):
    def __init__(self):
        super(OrdersController, self).__init__(OrdersService, OrderSchema)
