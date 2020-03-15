import click
from flask.cli import with_appcontext
from .extensions import guard, db
from .resources._auth.schema import User as GuardUser


@click.command(name="conf_db")
@click.option("--mode")
@with_appcontext
def conf_db(mode: str = "build"):
    if mode == "build":
        db.create_all()
    elif mode == "reset":
        db.drop_all()
        db.create_all()
    else:
        print("parameter mode may be either build or reset")


@click.command(name="create_admin")
@click.option("--password")
@with_appcontext
def create_admin(password):
    db.session.add(GuardUser(username="admin", password=guard.hash_password(password), roles="admin"))
    db.session.commit()
