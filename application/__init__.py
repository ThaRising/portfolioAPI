from flask import Flask
from .extensions import db, ma, api, guard, limit
from inspect import isclass
from .config import Prod, Stag


def create_app(env: any = ""):
    app = Flask(__name__, instance_relative_config=False)
    if isclass(env):
        app.config.from_object(env())
    else:
        app.config.from_object(Stag if not env else Prod)

    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    from .resources._auth.schema import User as GuardUser
    guard.init_app(app, GuardUser)
    limit.init_app(app)

    from .commands import conf_db, create_admin
    app.cli.add_command(conf_db)
    app.cli.add_command(create_admin)

    with app.app_context():
        from .shared.exceptions import handle_ambiguous_type, handle_auth_error, handle_ambiguous_fields
        from .resources.shop_digital.schema import ShopDigital
        from .resources import portfolio_api, shop_api, Auth
        api.add_namespace(portfolio_api, path="/portfolio")
        api.add_namespace(shop_api, path="/shop")
        app.add_url_rule('/login/', view_func=Auth.as_view('auth'))

        @app.after_request
        def add_headers(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = \
                "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
            response.headers['Access-Control-Allow-Methods'] = "POST, GET, PATCH, DELETE"
            return response

        return app


__all__ = ["create_app"]
