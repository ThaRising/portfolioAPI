from ...shared import Service
from .schema import Image


class ImageService(Service):
    def __init__(self):
        super(ImageService, self).__init__(Image)
