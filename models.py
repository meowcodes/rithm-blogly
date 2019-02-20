"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

DEFAULT_IMG_URL = "https://www3.nd.edu/~streslab/assets/img/ra_pics/Placeholder_Photo.png"

def connect_db(app):
    """ Connects to Database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ Users """"

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(50),
                            nullable= False)
    last_name = db.Column(db.String(50),
                            nullable= False)
    image_url = db.Column(db.Text,
                            default= DEFAULT_IMG_URL)
    