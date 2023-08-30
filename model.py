

""""""""""""""""""""""""""""""""""""""""""
"""  ###  PostgreSQL  Model  File ###  """
""""""""""""""""""""""""""""""""""""""""""
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

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
    bio = db.Column(db.TEXT)
    password_hash = db.Column(db.VARCHAR, nullable=False)
    isArtist = db.Column(db.Boolean, default=False)
    isModerator = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    user_image_url = db.Column(db.VARCHAR)

""" Post Table """
class Post(db.Model):
    __tablename__ = 'posts'
    
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    image_url = db.Column(db.VARCHAR, unique=True, nullable=False)
    image_blob = db.Column(db.LargeBinary)
    caption = db.Column(db.VARCHAR)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    
    def serialize(self):
        return {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'author': db.session.query(User).filter(User.user_id == self.user_id).first(),
            'image_url': self.image_url,
            'image_blob': self.image_blob,
            'caption': self.caption,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'likes': db.session.query(Like).filter(Like.post_id == self.post_id).count(),
            'favorites': db.session.query(Favorite).filter(Favorite.post_id == self.post_id).count(),
            'stars': db.session.query(Star).filter(Star.post_id == self.post_id).count()
        }


""" Comment Table """
class Comment(db.Model):
    __tablename__ = 'comments'
    
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
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
    

""" Tag Table """
class Tag(db.Model):
    __tablename__ = 'tag_table'
    
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.VARCHAR, unique=True, nullable=False)


""" Posted Tag Table """
class PostedTag(db.Model):
    __tablename__ = 'posted_tag'
    post_tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag_table.tag_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))


""" Like Table """
class Like(db.Model):
    __tablename__ = 'like_table'
    
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP)


""" Favorite Table """
class Favorite(db.Model):
    __tablename__ = 'favorite_table'
    
    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP)


""" Like Table """
class Star(db.Model):
    __tablename__ = 'star_table'
    
    star_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    
    
class ContentReport(db.Model):
    __tablename__ = 'content_reports'
    
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_user = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), nullable=True)
    is_hateful = db.Column(db.Boolean, nullable=True)
    is_spam = db.Column(db.Boolean, nullable=True)
    is_violent = db.Column(db.Boolean, nullable=True)
    is_explicit = db.Column(db.Boolean, nullable=True)
    is_other_report = db.Column(db.Boolean, nullable=True)
    original_report_note = db.Column(db.String, nullable=True)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    


""""""""""""""""""""""""""""""""""""""""""
""" ###       Database Config      ### """
""""""""""""""""""""""""""""""""""""""""""

def connect_to_db(flask_app, echo=True):

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")    
