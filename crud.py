from model import db, User, Tag, Post
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import jsonify

""""""""""""""""""""""""""""""""""""""""""
"""       ### CRUD Funtions ###        """
""""""""""""""""""""""""""""""""""""""""""

"""     Create      """
# create user
def create_user(username, email, password):
    print('creating new user')
    password_hash = generate_password_hash(password)
    user = User(
        username = username,
        email = email,
        password_hash = password_hash,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    db.session.add(user)
    db.session.commit()


# create tag
def create_new_tag(tag_name):
    tag = Tag(
        tag_name = tag_name
    )
    db.session.add(tag)
    db.session.commit()
    
    tag_data = { 'tag_name': tag.tag_name }
    return tag_data

# new post
def add_new_post(username, image_url, post_title):
    
    user_id = get_user_by_username(username).user_id
    
    post = Post(
        user_id = user_id,
        image_url = image_url,
        caption = post_title,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    db.session.add(post)
    db.session.commit()
    
    return post
    

"""      Read       """
# get all users
def get_users():
    return User.query.all()

# get user by id
def get_user_by_id(user_id):
    return User.query.get(user_id)

# get user by email
def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

# get user by username
def get_user_by_username(username):
    return User.query.filter(User.username == username).first()

def get_tags_from_substring(substring):
    substring = substring.lower()
    tags = Tag.query.filter(Tag.tag_name.ilike(f'{substring}%')).all()
    tags_data = [{'id': tag.tag_id, 'name': tag.tag_name} for tag in tags]
    return jsonify(tags_data)

def get_tag_from_name(tag_name):
    tag_name = tag_name.lower()
    tag = Tag.query.filter(Tag.tag_name == tag_name).first()
    if tag is None:
        return jsonify({'error': 'Tag not found'})

    tag_data = {'id': tag.tag_id, 'name': tag.tag_name}
    return jsonify(tag_data)


def get_users_images(username):
    user = get_user_by_username(username)
    post_query = Post.query.filter(Post.user_id == user.user_id).all()
    image_list = [{'id': post.post_id, 'url': post.image_url, 'caption': post.caption} for post in post_query]
    
"""     Update      """


"""     Delete      """



""""""""""""""""""""""""""""""""""""""""""
"""  ###     Server Methods     ###    """
""""""""""""""""""""""""""""""""""""""""""