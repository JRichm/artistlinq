from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, url_for
import crud

def login(loginForm):
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
    
    return redirect(url_for('login'))  # Return a valid response
                
def create_user(newUserForm):
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
    
    return redirect(url_for('login'))  # Return a valid response