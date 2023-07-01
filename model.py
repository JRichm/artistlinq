



""""""""""""""""""""""""""""""""""""""""""
"""  ###  PostgreSQL  Model  File ###  """
""""""""""""""""""""""""""""""""""""""""""
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


""""""""""""""""""""""""""""""""""""""""""
""" ###      PostgreSQL Tables     ### """
""""""""""""""""""""""""""""""""""""""""""

""" Users Table """
class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR, unique=True, nullable=False)
    email = db.Column(db.VARCHAR, unique=True, nullable=False)
    password_hash = db.Column(db.VARCHAR, nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)


""" Image Table """
class Image(db.Model):
    __tablename__ = 'images'
    
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    image_url = db.Column(db.VARCHAR, unique=True, nullable=False)
    caption = db.Column(db.VARCHAR)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)


""" Comment Table """
class Comment(db.Model):
    __tablename__ = 'comments'
    
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), nullable=False)
    comment_text = db.Column(db.VARCHAR)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    

""" Commission Request Table """
class CommissionRequest(db.Model):
    __tablename__ = 'commission_requests'
    
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    request_text = db.Column(db.VARCHAR)
    status = db.Column(db.VARCHAR)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

""" Artist Table """
class Artists(db.Model):
    __tablename__ = 'artists'
    
    artist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    bio = db.Column(db.TEXT)
    skills = db.Column(db.ARRAY(db.VARCHAR))
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)


""" Like Table """
class Likes(db.Model):
    __tablename__ = 'likes'
    
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    

""""""""""""""""""""""""""""""""""""""""""
""" ###       Database Config      ### """
""""""""""""""""""""""""""""""""""""""""""

def connect_to_db(flask_app, db_uri="postgresql:///art_station", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
