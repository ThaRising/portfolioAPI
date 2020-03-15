from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api
from flask_praetorian import Praetorian
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
ma = Marshmallow()
api = Api(doc=False)
guard = Praetorian()
limit = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "150 per hour"]
)
