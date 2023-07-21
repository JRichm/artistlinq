


from model import db, User, Tag, Post, PostedTag, Comment, Like, Favorite, Star, ContentReport
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import jsonify, session
from sqlalchemy import func

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


def add_tag_to_post(tag_id, post_id):
    tag = PostedTag(
        tag_id = tag_id,
        post_id = post_id
    )
    
    db.session.add(tag)
    db.session.commit()
    
    
def post_comment(user_id, post_id, comment_data): 
    comment = Comment(
        user_id=user_id,
        post_id=post_id,
        comment_text=comment_data,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.session.add(comment)
    db.session.commit()


def add_like_to_post(post_id, user_id):
    like = Like(
        user_id=user_id,
        post_id=post_id,
        created_at=datetime.now()
    )
    
    db.session.add(like)
    db.session.commit()


def add_post_to_favorites(post_id, user_id):
    favorite = Favorite(
        user_id=user_id,
        post_id=post_id,
        created_at=datetime.now()
    )
    
    db.session.add(favorite)
    db.session.commit()


def add_star_to_post(post_id, user_id):
    star = Star(
        user_id=user_id,
        post_id=post_id,
        created_at=datetime.now()
    )
    
    db.session.add(star)
    db.session.commit()
    
    
def new_report(report_user, post_id, comment_id,
               is_hateful, is_spam, is_violent, is_explicit, is_other_report,
               original_report_note):
    print('\n\nmaking new report\n\n')
    report = ContentReport(
                   report_user=report_user,
                   post_id=post_id,
                   comment_id=comment_id,
                   is_hateful=is_hateful,
                   is_spam=is_spam,
                   is_violent=is_violent,
                   is_explicit=is_explicit,
                   is_other_report=is_other_report,
                   original_report_note=original_report_note,
                   created_at=datetime.now(),
                   updated_at=datetime.now()
               )
    
    db.session.add(report)
    db.session.commit()


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
    return tag_data

def get_post_from_id(post_id):
    return Post.query.get(post_id)

def get_tags_from_post_id(post_id):
    tag_query = db.session.query(Tag.tag_name).join(PostedTag).filter(PostedTag.post_id == post_id).all()
    tag_list = [{'tag_name': tag.tag_name} for tag in tag_query]
    return tag_list

def get_posted_tags_from_post(post_id):
    tag_query = db.session.query(PostedTag).filter(PostedTag.post_id == post_id).all()
    tag_list = [{'post_tag_id': tag.post_tag_id, 'tag_id': tag.tag_id, 'post_id': tag.post_id} for tag in tag_query]
    return tag_list

def get_users_images(user_id):
    post_query = Post.query.filter(Post.user_id == user_id).all()
    image_list = [{'id': post.post_id, 'url': post.image_url, 'caption': post.caption} for post in post_query]
    return image_list

def get_50_images():
    post_query = db.session.query(Post).order_by(Post.post_id.desc()).limit(50).all()
    image_list = [{'id': post.post_id, 'user_id': post.user_id, 'url': post.image_url, 'caption': post.caption} for post in post_query]
    return image_list

def get_featured_users():
    user_query = db.session.query(User).order_by(User.user_id.desc()).limit(5).all()
    user_list = [{'id': user.user_id, 'username': user.username, 'created_at': user.created_at, 'updated_at': user.updated_at} for user in user_query]
    return user_list

def get_comments_from_post_id(post_id):
    comment_query = db.session.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.comment_id.desc()).all()
    comment_list = [{'comment_id': comment.comment_id,
                     'user_id': comment.user_id,
                     'username': get_user_by_id(comment.user_id).username,
                     'post_id': comment.post_id,
                     'comment_text': comment.comment_text,
                     'created_at': comment.created_at,
                     'updated_at': comment.updated_at} for comment in comment_query]
    return comment_list

def get_user_like_data(post_id, user_id):
    like_query = db.session.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
    fav_query = db.session.query(Favorite).filter(Favorite.post_id == post_id, Favorite.user_id == user_id).first()
    star_query = db.session.query(Star).filter(Star.post_id == post_id, Star.user_id == user_id).first()
    
    return [
        bool(like_query),
        bool(fav_query),
        bool(star_query)
    ]
    
def get_comments_with_reports():
    comments_with_reports = db.session.query(
        Comment,
        User.username,
        func.count(ContentReport.report_id).label('num_reports')
    ).outerjoin(ContentReport, Comment.comment_id == ContentReport.comment_id)\
    .join(User, Comment.user_id == User.user_id)\
    .group_by(Comment.comment_id, User.username)\
    .order_by(func.count(ContentReport.report_id).desc())\
    .all()

    # comments_with_reports will be a list of tuples where each tuple contains the Comment object and the number of reports.
    return comments_with_reports

    
def get_posts_with_reports():
    posts_with_reports = db.session.query(
        Post,
        User.username,
        func.count(ContentReport.report_id).label('num_reports')
    ).outerjoin(ContentReport, Post.post_id == ContentReport.post_id)\
    .join(User, Post.user_id == User.user_id)\
    .group_by(Post.post_id, User.username)\
    .order_by(func.count(ContentReport.report_id).desc())\
    .all()

    # posts_with_reports will be a list of tuples where each tuple contains the Post object, the username, and the number of reports.
    return posts_with_reports

def get_reports_for_post(post_id):
    reports = db.session.query(ContentReport).filter_by(post_id=post_id).all()
    return reports
    
    
"""     Update      """
def update_username(user_id, new_username):
    get_user_by_id(user_id).username = new_username
    db.session.commit()

def update_email(user_id, new_email):
    get_user_by_id(user_id).email = new_email
    db.session.commit()

def update_password(user_id, new_password_hash):
    get_user_by_id(user_id).password_hash = new_password_hash
    db.session.commit()

def update_bio(user_id, new_bio):
    get_user_by_id(user_id).bio = new_bio
    db.session.commit()


def setMod(user_id):
    print('\n\n\n\n\n\n new mod')
    user = get_user_by_id(user_id)
    user.isModerator = True
    db.session.commit()
    
    
"""     Delete      """

def delete_post(post_id):
    # remove related entries from the comment table
    comments = Comment.query.filter_by(post_id=post_id).all()
    for comment in comments:
        db.session.delete(comment)
    
    # Remove related entries from the like_table
    likes = Like.query.filter_by(post_id=post_id).all()
    for like in likes:
        db.session.delete(like)
    
    # Remove related entries from the favorite_table
    favorites = Favorite.query.filter_by(post_id=post_id).all()
    for favorite in favorites:
        db.session.delete(favorite)
    
    # Remove related entries from the star_table
    stars = Star.query.filter_by(post_id=post_id).all()
    for star in stars:
        db.session.delete(star)

    # Remove related entries from the posted_tag table
    posted_tags = PostedTag.query.filter_by(post_id=post_id).all()
    for posted_tag in posted_tags:
        db.session.delete(posted_tag)

    # Now delete the post instance
    post = get_post_from_id(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()

def remove_like_from_post(post_id, user_id):
    like = db.session.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()

def remove_post_from_favorites(post_id, user_id):
    favorite = db.session.query(Favorite).filter(Favorite.post_id == post_id, Favorite.user_id == user_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()

def remove_star_from_post(post_id, user_id):
    star = db.session.query(Star).filter(Star.post_id == post_id, Star.user_id == user_id).first()
    if star:
        db.session.delete(star)
        db.session.commit()

""""""""""""""""""""""""""""""""""""""""""
"""  ###     Server Methods     ###    """
""""""""""""""""""""""""""""""""""""""""""