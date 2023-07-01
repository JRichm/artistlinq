

""""""""""""""""""""""""""""""""""""""""""
"""      ### Server Imports ###        """
""""""""""""""""""""""""""""""""""""""""""
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, request, url_for, flash
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
    return render_template('index.html')
  
  
    ### " View Login/New User" ###
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = forms.LoginForm()
    newUserForm = forms.RegistrationForm()
    
    print('login function called')
    print('login button value:', request.form.get('login'))
    print('new-user button value:', request.form.get('new-user'))
    
    if request.form.get('login') == 'Login':
        print('Process login form submission')
        if loginForm.validate_on_submit():
            # Process login form submission
            username = loginForm.username.data
            password = loginForm.password.data
            user = crud.get_user_by_username(username)
            if user and check_password_hash(user.password_hash, password):
                # Authentication successful
                return redirect(url_for('index'))
            else:
                flash('invalid deets')
                # flash('Invalid username or password. Please try again.')
        
    elif request.form.get('new-user') == 'Create Account':
        print('Process new user form submission')
        if newUserForm.validate_on_submit():
            # Process new user form submission
            username = newUserForm.username.data
            password = newUserForm.password.data
            email = newUserForm.email.data
            if crud.get_user_by_username(username):
                flash('Username already exists. Please choose a different username.')
            else:
                # Generate password hash with salt
                crud.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                flash('Account created successfully!')
                return redirect(url_for('index'))
    return render_template('login.html', loginForm=loginForm, newUserForm=newUserForm)


""""""""""""""""""""""""""""""""""""""""""
"""  ###     Server Methods     ###    """
""""""""""""""""""""""""""""""""""""""""""
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)