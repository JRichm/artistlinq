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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

""""""""""""""""""""""""""""""""""""""""""
"""     ###    Flask Routes    ###     """
""""""""""""""""""""""""""""""""""""""""""

    ### " View Homepage " ###
@app.route('/')
def index():
    return render_template('index.html', images=get_images())
  
  
    ### " View Login/New User" ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = forms.LoginForm()
    newUserForm = forms.RegistrationForm()
    
    if request.form.get('login') == 'Login':
        return loginForm.login()
        
    elif request.form.get('new-user') == 'Create Account':
        return newUserForm.create_user()
        
    return render_template('login.html', loginForm=loginForm, newUserForm=newUserForm)
  

    ### " View User " ###
@app.route('/user/<username>')
def user_view(username):
    user = crud.get_user_by_username(username)
    return render_template('user_view.html', user=user, images=get_images())


    ### " New Post " ###
@app.route('/post')
def new_post():
    return render_template('new_post.html')

@app.route('publish_post', methods=['POST'])
def publish_new_post():
    post_data = request.get_json()
    post_title = post_data.get('title')
    post_tags = post_data.get('tags')
    post_description = post_data.data.get('description')
    post_file = post_data.get('file')
    user_id = session.get('user_id')
    
    new_post = crud.publish_post(post_title, post_tags, post_file, post_description, user_id)


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


""""""""""""""""""""""""""""""""""""""""""
"""  ###     Server Methods     ###    """
""""""""""""""""""""""""""""""""""""""""""
    ### " Temporary images " ###
def get_images():
    image_folder = './static/images/'
    images = []
    
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            image_url = '/static/images/' + filename
            images.append({'path': image_path, 'url': image_url})
            
    return images

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)