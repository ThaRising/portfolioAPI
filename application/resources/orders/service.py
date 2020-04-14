from application.shared import Service
from .schema import Order


class OrdersService(Service):
    def __init__(self):
        super(OrdersService, self).__init__(Order)
