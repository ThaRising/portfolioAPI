from flask_praetorian import PraetorianError
from webargs.flaskparser import use_kwargs
from .schema import UserSchema
from ...extensions import guard, limit
from flask import abort
from flask import make_response
from flask.views import MethodView


class Auth(MethodView):
    decorators = [limit.limit("3/minute;5/hour;10/day")]

    @use_kwargs(UserSchema, locations=("json",))
    def post(self, **kwargs):
        try:
            user = guard.authenticate(kwargs.get("username"), kwargs.get("password"))
        except PraetorianError:
            abort(401, "Invalid Credentials.")
        return make_response({'access_token': guard.encode_jwt_token(user)}, 200)
