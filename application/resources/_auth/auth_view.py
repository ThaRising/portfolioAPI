from flask_praetorian import PraetorianError
from webargs.flaskparser import use_kwargs
from .schema import UserSchema
from ...extensions import guard, limit
from flask import abort
from flask import make_response
from flask.views import MethodView
from flask_praetorian import auth_required


class Auth(MethodView):
    decorators = [limit.limit("5/minute;10/hour;25/day")]

    @auth_required
    def get(self):
        return make_response("Valid", 200)

    @use_kwargs(UserSchema, locations=("json",))
    def post(self, **kwargs):
        try:
            user = guard.authenticate(kwargs.get("username"), kwargs.get("password"))
        except PraetorianError:
            abort(401, "Invalid Credentials.")
        return make_response({'access_token': guard.encode_jwt_token(user)}, 200)
