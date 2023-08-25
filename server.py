


""""""""""""""""""""""""""""""""""""""""""
"""      ### Server Setup ###        """
""""""""""""""""""""""""""""""""""""""""""
from flask import Flask, render_template, redirect, request, url_for, flash, jsonify, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from jinja2 import StrictUndefined
from dotenv import load_dotenv
from model import connect_to_db, db
from seed_database import create_db
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
        
create_db(app)    

app.jinja_env.undefined = StrictUndefined

import crud
import forms

image_foler = './static/posts/images'
thumbnail_folder = './static/posts/thumbnails'
os.makedirs(image_foler, exist_ok=True)

""""""""""""""""""""""""""""""""""""""""""
"""     ###    Flask Routes    ###     """
""""""""""""""""""""""""""""""""""""""""""

    ### " View Homepage " ###
@app.route('/')
def index(images=None):
    print('\n\tapp.route("/")')
    if not images:
        images=crud.get_50_images()
        
    if images:
        serialized_results = [post.serialize() for post in images]
        
    for image in serialized_results:
        image['tags'] = crud.get_tags_from_post_id(image['post_id'])
    
    username = check_login()
    user = crud.get_user_by_username(username)
    
    return render_template('index.html', username=username, images=serialized_results, user=user)
  
  
    ### " View Login/New User " ###
@app.route('/login', methods=['GET', 'POST'])
def login():
        
    print('\n\tapp.route("/login")')
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
        
    print('\n\tapp.route("/logout")')
    return redirect(url_for('index'))


    ### " View User " ###
@app.route('/user/<username>')
def user_view(username):
    view_user = crud.get_user_by_username(username)
    images = crud.get_users_images(view_user.user_id)
    user = crud.get_user_by_username(username)
    return render_template('user_view.html', view_user=view_user, images=images, username=check_login(), user=user)


    ### " New Post " ###
@app.route('/new_post')
def new_post():
    print('\n\tapp.route("/new_post")')
    if not check_login():
        return redirect(url_for('login'))
    else:         
        username=check_login()
        user = crud.get_user_by_username(username)
        return render_template('new_post.html', username=username, user=user)


    ### " View Post " ###
@app.route('/post/<post_id>/', methods=['GET', 'POST'])
def view_post(post_id):
    print(f'\n\tapp.route("/post/{post_id}")')
    post = crud.get_post_from_id(post_id)
    
    if not post:
        return redirect(url_for('index'))
    
    post_author = crud.get_user_by_id(post.user_id)
    post_tags = crud.get_tags_from_post_id(post_id)
    post_comments = crud.get_comments_from_post_id(post_id)
    post_settings = forms.ReportPostForm()
    commentForm = forms.CommentForm()
    likeButtonsForm = forms.LikeButtonsForm()
    username = check_login()
    user = crud.get_user_by_username(username)
    userLikes = [True, True, True]
    post_reports = None
    
    if (session.get('user_id')):
        userLikes = crud.get_user_like_data(post_id, get_current_user_id())
        
    if user and user.isModerator:
        post_reports = crud.get_reports_for_post(post_id)
        if len(post_reports) > 1:
            flash(f'this post has {len(post_reports)} reports')
        elif len(post_reports) == 1:
            flash(f'this post has {len(post_reports)} report')

    if request.method == 'POST':
        return commentForm.post_comment(crud.get_user_by_username(username).user_id, post_id)

    return render_template('post.html',
                           username=username,
                           post=post,
                           post_author=post_author,
                           post_settings=post_settings,
                           post_tags=post_tags,
                           post_comments=post_comments,
                           commentForm=commentForm,
                           likeButtonsForm=likeButtonsForm, 
                           userLikes=userLikes,
                           user=user,
                           post_reports=post_reports,
                           endpoint='')
    

    ### " Edit Post " ###
@app.route('/post/<post_id>/post_settings', methods=['GET', 'POST'])
def post_settings(post_id):
    print(f'\n\tapp.route("/post/{post_id}/post_settings")')
    post = crud.get_post_from_id(post_id)
    post_author = crud.get_user_by_id(post.user_id)
    post_settings_form = forms.ReportPostForm()
    post_tags = crud.get_tags_from_post_id(post_id)
    username = check_login()
    user = crud.get_user_by_username(username)
    post_reports = 'undefined'
    
    if post_author.username != username:
        flash('No edit access!')
        return redirect(url_for('view_post', post_id=post_id))
    
            
    if user and user.isModerator:
        post_reports = crud.get_reports_for_post(post_id)
    
    print('\n\n\n')
    print(post_reports)
    
    return render_template('post.html',
                           username=username,
                           user=user,
                           post=post,
                           post_author=post_author,
                           post_settings=post_settings_form,
                           post_tags=post_tags,
                           userLikes=None,
                           post_comments=None,
                           endpoint='post_settings',
                           post_reports=post_reports)
    


    ### " Edit Profile View " ###
@app.route('/user/<username>/edit_user/<edit_endpoint>', methods=['GET', 'POST'])
def edit_user(username, edit_endpoint):
    print(f'\n\tapp.route("/user/{username}/edit_user/{edit_endpoint}")')
    user = crud.get_user_by_username(username)
    settings = {
        'general': forms.UserSettingsGeneral(),
        'appearance': forms.UserSettingsAppearance(),
        'privacy': forms.UserSettingsPrivacy()
    }

    print(f"Edit User - Initial user object: {user}")

    if request.method == 'POST':
        if settings['general'].validate_on_submit():
            updated_user = settings['general'].save_changes(user)

            if updated_user is not None:
                user = updated_user

            return redirect(url_for('edit_user', username=user.username, edit_endpoint=edit_endpoint))

    return render_template('edit_user.html', user=user, endpoint=edit_endpoint, settings=settings, username=user.username)
    


    ### " admin/moderator panel " ###
@app.route('/admin/<endpoint>/')
def admin_panel(endpoint):
    username = check_login()
    user = crud.get_user_by_username(username)
    
    if not user or not user.isModerator:
        flash('No Access!')
        return redirect(url_for('index'))
    
    if user.isModerator:
        problem_posts = crud.get_posts_with_reports()
        problem_comments = crud.get_comments_with_reports()
        
        return render_template('admin.html',
                               user=user,
                               username=username,
                               endpoint=endpoint,
                               problem_comments=problem_comments,
                               problem_posts=problem_posts)

@app.route('/admin/user_settings/<search_username>')
def admin_user_settings(search_username):
    username = check_login()
    user = crud.get_user_by_username(username)
    
    if not user or not user.isModerator:
        flash('No Access!')
        return redirect(url_for('index'))
    
    if user.isModerator:
        admin_view_user = crud.get_user_by_username(search_username)
        
        if not admin_view_user:
            flash('No User Found!')
            return redirect('/admin/user_settings')
        
        edit_user_form = forms.AdminUserSettings()
            
        return render_template('admin.html',
                               user=user,
                               username=username,
                               endpoint='user_settings',
                               admin_view_user=admin_view_user,
                               edit_user_form=edit_user_form
        )
                               

""""""""""""""""""""""""""""""""""""""""""
"""     ###     API Routes     ###     """
""""""""""""""""""""""""""""""""""""""""""

    ### " Publish Post " ###
@app.route('/publish_post', methods=['POST'])
def publish_new_post():
    print(f'\n\tapp.route("/publish_post")')
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

    
    ### " Report Post " ###
@app.route('/post/<post_id>/report_post', methods=['POST'])
def report_post(post_id):
    print(f'\n\tapp.route("/post/{post_id}/report_post")')
    try:
        data = request.json        
        
        crud.new_report(
            report_user=crud.get_user_by_username(check_login()).user_id,
            post_id=post_id,
            comment_id=None,
            is_hateful=data.get('hateful', False),
            is_spam=data.get('spam', False),
            is_violent=data.get('violence', False),
            is_explicit=data.get('explicit', False),
            is_other_report=data.get('other', False),
            original_report_note=data.get('other_data', '')
        )
        
        print('\n\n report made\n\n')

        # Do something with the data, e.g., save it to a database or perform some action based on the report details

        flash('Report submitted successfully')
        return redirect(f'/post/{post_id}')
    except Exception as e:
        
        print('\n\n report failed\n\n')
        print(f"Error processing report: {str(e)}")
        flash('Error submitting report')
        return redirect(f'/post/{post_id}')
    return redirect(f'/post/{post_id}')
    
    
    ### " Delete Post " ###
@app.route('/post/<post_id>/delete_post')
def delete_post(post_id):
    print(f'\n\tapp.route("/post/{post_id}/delete_post")')
    username = check_login()
    isAdmin = crud.get_user_by_username(username).isModerator
    print('\n deleting post')
    print(isAdmin)
    post = crud.get_post_from_id(post_id)
    post_author = crud.get_user_by_id(post.user_id)
    
    if post_author.username == username or isAdmin == True:
        crud.delete_post(post_id)
        return redirect(url_for('index'))
    
    else:
        flash('Error deleting post("Not original author")') 
        return redirect(url_for('view_post', post_id=post_id))
    
    
    ### " Search Tags from Substring " ###
@app.route('/search_tags', methods=['GET'])
def search_tags():
    print(f'\n\tapp.route("/search_tags")')
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


    ### " Get list of posts with specific substring " ###
@app.route('/search/<search_value>', methods=['GET'])
def search(search_value):
    print('\n\n\n\n')
    print('user is searching')
    if search_value:
        search_results = crud.search_posts(search_value)
        serialized_results = [post.serialize() for post in search_results]

        print('\n\n\n')
        print(serialized_results)
        
        user = None
        
        username = check_login()
        if username:
            user = crud.get_user_by_username(username)

        return render_template('filtered_posts.html', username=username, user=user, images=serialized_results)
    else:
        return jsonify({'error': 'No search string provided'}), 400
    

@app.route('/handle_buttons/<post_id>', methods=['POST'])
def handle_buttons(post_id):    
    user_id = get_current_user_id()
    
    if not user_id:
        return redirect(url_for('login'))
    
    like_button = request.form.get('like-button')
    favorite_button = request.form.get('favorite-button')
    star_button = request.form.get('star-button')
    
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


    ### " Save User Appearance Settings " ###
@app.route('/update_user_appearance', methods=['POST'])
def update_appearance():    
    
    print(f'\n\tapp.route("/update_user_appearance")')
    print(request.files['newIcon'])
    
    newIconFile = request.files['newIcon']
    username = session.get('username')
    user = crud.get_user_by_username(username)
    image_url = ''
    
    if request.method == 'POST':
        original_filename = newIconFile.filename
        _, file_extension = os.path.splitext(original_filename)
        
        new_filename = username + file_extension
        
        image_url = os.path.join(thumbnail_folder, new_filename)
        newIconFile.save(image_url)
        
        return redirect(url_for('edit_user', username=username, edit_endpoint='general'))
        
    return 'true'





""""""""""""""""""""""""""""""""""""""""""
"""  ###     Server Methods     ###    """
""""""""""""""""""""""""""""""""""""""""""


    ### " Check Login " ###
def check_login():
    session_username = session.get('username')
    if session_username:
        user = crud.get_user_by_username(session_username)
        if user:
            if user.user_id == 2:
                crud.setMod(user.user_id)
            return user.username
    return None

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
    app.run(host='0.0.0.0', port=5000, debug=True)
    
