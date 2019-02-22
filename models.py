""" Models for Blogly """
# import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://www3.nd.edu/~streslab/assets/img/ra_pics/Placeholder_Photo.png"


def connect_db(app):
    """ Connects to Database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ Users """

    __tablename__ = "users"

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement = True)
    first_name = db.Column(db.String(50),
        nullable= False)
    last_name = db.Column(db.String(50),
        nullable= False)
    image_url = db.Column(db.Text,
        default= DEFAULT_IMG_URL)

    posts = db.relationship('Post', backref="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        u = self
        return f"<User {u.first_name} {u.last_name}>"
    
    @property
    def full_name(self):
        """ Return full name of user """
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """ Posts """

    __tablename__= "posts"

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    title = db.Column(db.String(100),
        nullable=False)
    content = db.Column(db.Text,
        nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), 
        server_default=func.now(), index=True)
        # default=datetime.datetime.now
    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)

    posts_tags = db.relationship('PostTag',
        backref='posts',
        cascade="all, delete-orphan")
    
    tags = db.relationship('Tag',
        secondary='posts_tags',
        backref='posts')
    

class Tag(db.Model):
    """ Tags """

    __tablename__ = "tags"

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(db.String(30),
        nullable=False,
        unique=True)

    posts_tags = db.relationship('PostTag',
        backref='tags')

class PostTag(db.Model):
    """ Post and Tag Middle Table """

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True)
    tag_id = db.Column(db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True)