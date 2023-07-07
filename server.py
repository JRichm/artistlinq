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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

""""""""""""""""""""""""""""""""""""""""""
"""     ###    Flask Routes    ###     """
""""""""""""""""""""""""""""""""""""""""""

    ### " View Homepage " ###
@app.route('/')
def index():
    images=get_images()
    username = check_login()
    return render_template('index.html', username=username, images=images)
  
  
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
    return render_template('user_view.html', view_user=view_user, images=get_images())


    ### " New Post " ###
@app.route('/post')
def new_post():
    if not check_login():
        return redirect(url_for('login'))
    else: 
        return render_template('new_post.html')


    ### " Publish Post " ###
@app.route('/publish_post', methods=['POST'])
def publish_new_post():
    post_title = request.form['title']
    post_tags = request.form.getlist('tags')
    post_file = request.files['file']
    username = session.get('username')
    image_url = ''
    
    # Process the data, save the file, etc.
    print(post_title)
    print(post_tags)
    print(username)
    
    if request.method == 'POST':
        image_url = os.path.join(image_foler, post_file.filename)
        post_file.save(image_url)
        
        crud.add_new_post(username, image_url, post_title)
        
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
    view_username = request_data.get('username')
    return crud.get_users_images()
    
    




""""""""""""""""""""""""""""""""""""""""""
"""  ###     Server Methods     ###    """
""""""""""""""""""""""""""""""""""""""""""


    ### " Check Login " ###
def check_login():
    session['username'] = session.get('username') or None
    return crud.get_user_by_username(session['username']).username if session['username'] else None


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

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)