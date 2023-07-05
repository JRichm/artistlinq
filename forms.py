""" ### Flask Forms ### """

from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
import crud

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')
    
    def login(self):
        print('Process login form submission')
        if self.validate_on_submit():
            # Process login form submission
            username = self.username.data
            password = self.password.data
            user = crud.get_user_by_username(username)
            if user and check_password_hash(user.password_hash, password):
                # Authentication successful
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('invalid deets')
                # flash('Invalid username or password. Please try again.')
    
        return redirect(url_for('login'))  # Return a valid response


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Create Account')
    
    def create_user(self):
        print('Process new user form submission')
        if self.validate_on_submit():
            # Process new user form submission
            username = self.username.data
            password = self.password.data
            email = self.email.data
            if crud.get_user_by_username(username):
                flash('Username already exists. Please choose a different username.')
            else:
                # Generate password hash with salt
                crud.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                session['username'] = username
                flash('Account created successfully!')
                return redirect(url_for('index'))
        
        return redirect(url_for('login'))  # Return a valid response