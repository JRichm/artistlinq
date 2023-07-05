""""""""""""""""""""""""""""""""""""""""""
"""      ### Server Imports ###        """
""""""""""""""""""""""""""""""""""""""""""
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from model import connect_to_db, db
import controller
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
    image_folder = './static/images/'
    images = []
    
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            image_url = '/static/images/' + filename
            images.append({'path': image_path, 'url': image_url})
            
    
    return render_template('index.html', images=images)
  
  
    ### " View Login/New User" ###
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = forms.LoginForm()
    newUserForm = forms.RegistrationForm()
    
    if request.form.get('login') == 'Login':
        return controller.login(loginForm)
        
    elif request.form.get('new-user') == 'Create Account':
        return controller.create_user(newUserForm)
        
    return render_template('login.html', loginForm=loginForm, newUserForm=newUserForm)


""""""""""""""""""""""""""""""""""""""""""
"""  ###     Server Methods     ###    """
""""""""""""""""""""""""""""""""""""""""""
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)