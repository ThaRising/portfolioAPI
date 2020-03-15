from application.shared import Service
from application.resources.portfolio_image.schema import PortfolioImage


class PortfolioImageService(Service):
    def __init__(self):
        super(PortfolioImageService, self).__init__(PortfolioImage)
