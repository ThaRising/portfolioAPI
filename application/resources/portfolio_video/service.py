from application.shared import Service
from application.resources.portfolio_video.schema import PortfolioVideo


class PortfolioVideoService(Service):
    def __init__(self):
        super(PortfolioVideoService, self).__init__(PortfolioVideo)
