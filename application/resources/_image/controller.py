from ...shared import Controller
from .service import ImageService
from .schema import ImageSchema
from ...extensions import db
from random import choice
from string import ascii_letters
from datetime import datetime
from werkzeug.utils import secure_filename
import re
from binascii import a2b_base64
from flask import current_app
from pathlib import Path
from PIL import Image


class ImageController(Controller):
    def __init__(self):
        super(ImageController, self).__init__(ImageService, ImageSchema)

    def create(self, params: dict, **kwargs) -> db.Model:
        uri = a2b_base64(re.sub('^data:image/.+;base64,', '', params.get("uri")))
        random_chars = (lambda r: "".join([choice(ascii_letters) for i in range(r)]))
        filename = secure_filename(f"{datetime.now()}{random_chars(5)}.png")
        filepath: str = f"{current_app.config['IMAGE_UPLOADS'] / filename}"
        with open(filepath, 'wb') as f:
            f.write(uri)
        # Crop Preview Images to 16:9 Size
        if kwargs.get("preview", False):
            im = Image.open(filepath)
            width = im.size[0]
            height = im.size[1]
            aspect = width / float(height)
            ideal_aspect = 1920 / 1080
            if aspect > ideal_aspect:
                new_width = int(ideal_aspect * height)
                offset = (width - new_width) / 2
                resize = (offset, 0, width - offset, height)
            else:
                new_height = int(width / ideal_aspect)
                offset = (height - new_height) / 2
                resize = (0, offset, width, height - offset)
            cropped = im.crop(resize)
            cropped.save(filepath)
        return self.service().create({"uri": filename, "alt": params.get("alt")})

    def delete(self, key: int) -> None:
        delete_model = self.service().get({"id": key})[0]
        Path.unlink(current_app.config['IMAGE_UPLOADS'] / delete_model.uri)
        self.service().delete(key)
