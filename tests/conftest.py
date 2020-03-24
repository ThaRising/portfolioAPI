import pytest
from application import create_app
from application.extensions import db, guard
from application.resources._auth.schema import User
from application.resources.portfolio_image.schema import PortfolioImage
from application.resources.portfolio_video.schema import PortfolioVideo


class Testing:
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test_key"
    JWT_ACCESS_LIFESPAN = {'minutes': 30}
    JWT_REFRESH_LIFESPAN = {'minutes': 30}
    IMAGE_UPLOADS = "/uploads"


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(Testing)
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope="module")
def init_db():
    db.create_all()
    db.session.add(User(
        username="admin", password=guard.hash_password("admin"), roles="admin"
    ))
    db.session.add(PortfolioImage(
        title="Test", category="portrait", client="Der Boi"
    ))
    db.session.add(PortfolioVideo(
        title="Test", category="aftermovie", client="Der Boi", video="ilusrhgiur"
    ))
    db.session.commit()

    yield db

    db.drop_all()
