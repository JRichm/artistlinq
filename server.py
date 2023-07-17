


""""""""""""""""""""""""""""""""""""""""""
"""      ### Server Imports ###        """
""""""""""""""""""""""""""""""""""""""""""
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, request, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from model import connect_to_db, db
import forms
import crud
import os

image_foler = './static/posts/images'
os.makedirs(image_foler, exist_ok=True)

app = Flask(__name__, root_path=os.path.dirname(os.path.abspath(__file__)))
app.config['SECRET_KEY'] = 'dev'

""""""""""""""""""""""""""""""""""""""""""
"""     ###    Flask Routes    ###     """
""""""""""""""""""""""""""""""""""""""""""

    ### " View Homepage " ###
@app.route('/')
def index():
    images=crud.get_50_images()
    featured = crud.get_featured_users()
    username = check_login()
    return render_template('index.html', username=username, images=images, featured=featured)
  
  
    ### " View Login/New User " ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = forms.LoginForm()
    newUserForm = forms.RegistrationForm()
    
    if request.form.get('login') == 'Login':
        return loginForm.login()
        
    elif request.form.get('new-user') == 'Create Account':
        return newUserForm.create_user()
        
    return render_template('login.html', loginForm=loginForm, newUserForm=newUserForm)

  
    ### " User Logout " ###
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


    ### " View User " ###
@app.route('/user/<username>')
def user_view(username):
    view_user = crud.get_user_by_username(username)
    images = crud.get_users_images(view_user.user_id)
    return render_template('user_view.html', view_user=view_user, images=images, username=check_login())


    ### " New Post " ###
@app.route('/new_post')
def new_post():
    if not check_login():
        return redirect(url_for('login'))
    else: 
        return render_template('new_post.html', username=check_login())


    ### " View Post " ###
@app.route('/post/<post_id>/', methods=['GET', 'POST'])
def view_post(post_id):
    post = crud.get_post_from_id(post_id)
    post_author = crud.get_user_by_id(post.user_id)
    post_tags = crud.get_tags_from_post_id(post_id)
    post_comments = crud.get_comments_from_post_id(post_id)
    commentForm = forms.CommentForm()
    likeButtonsForm = forms.LikeButtonsForm()
    username = check_login()
    userLikes = [True, True, True]
    if (session.get('user_id')):
        userLikes = crud.get_user_like_data(post_id, get_current_user_id())

    if request.method == 'POST':
        return commentForm.post_comment(crud.get_user_by_username(username).user_id, post_id)

    return render_template('post.html',
                           username=username,
                           post=post,
                           post_author=post_author,
                           post_tags=post_tags,
                           post_comments=post_comments,
                           commentForm=commentForm,
                           likeButtonsForm=likeButtonsForm, 
                           userLikes=userLikes)
    

    ### " Edit Profile View " ###
@app.route('/user/<username>/edit_user')
def edit_user(username):
    return render_template('edit_user.html')

""""""""""""""""""""""""""""""""""""""""""
"""     ###     API Routes     ###     """
""""""""""""""""""""""""""""""""""""""""""

    ### " Publish Post " ###
@app.route('/publish_post', methods=['POST'])
def publish_new_post():
    post_title = request.form['title']
    post_tags = request.form.getlist('tags')
    post_file = request.files['file']
    username = session.get('username')
    image_url = ''
    
        
    if request.method == 'POST':
        image_url = os.path.join(image_foler, post_file.filename)
        post_file.save(image_url)
        
        post = crud.add_new_post(username, image_url, post_title)
        for tag_name in post_tags:
            tag = crud.get_tag_from_name(tag_name)
            crud.add_tag_to_post(tag['id'], post.post_id)
        
    return redirect(url_for('index'))


    ### " Search Tags from Substring " ###
@app.route('/search_tags', methods=['GET'])
def search_tags():
    search_key = request.args.get('key')
    tags = crud.get_tags_from_substring(search_key)
    return tags


    ### " Search Tags by name " ###
@app.route('/get_tag_by_name', methods=['GET'])
def get_tag_name():
    tag_name = request.args.get('tag')
    tag = crud.get_tag_from_name(tag_name)
    return tag


    ### " Search Tags by name " ###
@app.route('/create_new_tag', methods=['POST'])
def create_new_tag():
    tag_data = request.get_json()
    tag_name = tag_data.get('tag')
    return crud.create_new_tag(tag_name)


    ### " Get users images " ###
@app.route('/get_users_images', methods=['GET'])
def get_users_images():
    request_data = request.get_json()
    view_user = crud.get_user_by_username(request_data.get('username'))
    return crud.get_users_images(view_user.user_id)


@app.route('/handle_buttons/<post_id>', methods=['POST'])
def handle_buttons(post_id):
    
    print('\n\n\n\n\ntime to handle buttons:')
    
    like_button = request.form.get('like-button')
    favorite_button = request.form.get('favorite-button')
    star_button = request.form.get('star-button')
    
    print(session.get('username'))
    
    user_id = get_current_user_id()
    likeData = crud.get_user_like_data(post_id, user_id)
        
    if like_button == 'like':
        if (likeData[0]):
            crud.remove_like_from_post(post_id=post_id, user_id=user_id)
        else:
            crud.add_like_to_post(post_id=post_id, user_id=user_id)
        
    if favorite_button == 'favorite':
        if (likeData[1]):
            crud.remove_post_from_favorites(post_id=post_id, user_id=user_id)
        else:
            crud.add_post_to_favorites(post_id=post_id, user_id=user_id)
        
    if star_button == 'star':
        if (likeData[2]):
            crud.remove_star_from_post(post_id=post_id, user_id=user_id)
        else:
            crud.add_star_to_post(post_id=post_id, user_id=user_id)
        
    return redirect(url_for('view_post', post_id=post_id))


""""""""""""""""""""""""""""""""""""""""""
"""  ###     Server Methods     ###    """
""""""""""""""""""""""""""""""""""""""""""


    ### " Check Login " ###
def check_login():
    session['username'] = session.get('username') or None
    return crud.get_user_by_username(session['username']).username if session['username'] else None

def get_current_user_id():
    session['user_id'] = session.get('user_id') or None
    return crud.get_user_by_id(session['user_id']).user_id if session['user_id'] else None
    
    

    ### " Temporary images " ###
def get_images():
    
    image_folder = './static/posts/images/'
    images = []
    
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
            image_path = os.path.join(image_folder, filename)
            image_url = './static/posts/images/' + filename
            images.append({'path': image_path, 'url': image_url})
            
    return images

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in field '{getattr(form, field).label.text}': {error}", "error")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)