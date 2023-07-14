


""" ### Flask Forms ### """

from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from markupsafe import Markup
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
                session['user_id'] = user.user_id
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
                session['user_id'] = crud.get_user_by_username(username).user_id
                flash('Account created successfully!')
                return redirect(url_for('index'))
        
        return redirect(url_for('login'))  # Return a valid response
    

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()], render_kw={"placeholder": "leave a comment"})
    submit = SubmitField(validators=[DataRequired()], render_kw={"value": "post"})
    
    def post_comment(self, user_id, post_id):
        if self.validate_on_submit():
            comment_data = self.comment.data

            print('\n posting new comment')
            crud.post_comment(
                user_id=user_id,
                post_id=post_id,
                comment_data=comment_data
            )
            self.comment.data = ""
            
            return redirect(url_for(request.endpoint, post_id=post_id, _external=True, _anchor='comment-section'))
        
        print(self.errors)


class LikeButtonsForm(FlaskForm):
    like_button = SubmitField(validators=[DataRequired()], render_kw={"id": "like-button"})
    favorite_button = SubmitField(validators=[DataRequired()], render_kw={"id": "favorite-button"})
    star_button = SubmitField(validators=[DataRequired()], render_kw={"id": "star-button"})
