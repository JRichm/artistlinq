


""" ### Flask Forms ### """

from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField, BooleanField
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

class UserSettingsGeneral(FlaskForm):
    username = StringField('Username')
    email = StringField('Email')
    new_password = PasswordField('Update Password')
    new_password_confirm = PasswordField('Confirm Password')
    old_password = PasswordField('Current Password')
    bio = TextAreaField(render_kw={"placeholder": 'bio'})
    
    def save_changes(self, user):
        print(user.user_id)
        
        new_username_data = self.username.data
        new_email_data = self.email.data
        new_password_data = self.new_password.data
        new_password_confirm_data = self.new_password_confirm.data
        old_password_data = self.old_password.data
        new_bio_data = self.bio.data
            
        # Return if no input
        if not (new_username_data or new_password_data or new_email_data or new_bio_data):
            return None
        
        # Require password if user updating username, password or email
        if new_username_data or new_password_data or new_email_data:
            if not old_password_data:
                self.old_password.errors.append("Please enter password to update username/email/password")
                flash("Please enter password to update username/email/password")
                print('\nreturn: no password')
                return None

            # validate old password
            elif not check_password_hash(user.password_hash, old_password_data):
                flash("Incorrect password! Try again")
                self.old_password.errors.append("Incorrect password")
                print('\nreturn: wrong password\n')
                return None
            
            # updating username
            if new_username_data:
                existing_user = crud.get_user_by_username(new_username_data)
                if existing_user:
                    flash('Username already in use!')
                    self.username.errors.append("Username in use")
                    print('\nreturn: username in use\n')
                    return None
                else:
                    user.username = new_username_data
                    crud.update_username(user.user_id, user.username)
                    session['username'] = user.username
                    print('\n**\n\tupdated username!\n**\n')
                    
            # updating email
            if new_email_data:
                existing_user = crud.get_user_by_username(new_username_data)
                if existing_user:
                    flash('Email already in use!')
                    self.email.errors.append("Email in use")
                    print('\nreturn: email in use\n')
                    return None
                else:
                    user.email = new_email_data
                    crud.update_email(user.user_id, user.email)
                    print('\n**\n\tupdated email!\n**\n')
            
            # updating password
            if new_password_data or new_password_confirm_data:
                if new_password_data != new_password_confirm_data:
                    flash("Passwords do not match")
                    self.new_password.errors.append("Passwords do not match")
                    return None
                else:
                    user.password_hash = generate_password_hash(new_password_data)
                    crud.update_password(user.user_id, user.password_hash)
                    print('\n**\n\tupdated password!\n**\n')
                    
        if new_bio_data:
            user.bio = new_bio_data
            crud.update_bio(user.user_id, user.bio)

        flash("User profile updated successfully.")
        return user
    
    
class UserSettingsAppearance(FlaskForm):
    new_icon = FileField('User Icon', render_kw={'id': 'new-icon-input'})
    new_background = FileField('Profile Background')
    

class UserSettingsPrivacy(FlaskForm):
    see_me = SelectField('Who can view my profile?', choices=[('anyone', 'Anyone'), ('followers', 'Followers'), ('only-me', 'Only Me')])
    message_me = SelectField('Who can message me?', choices=[('anyone', 'Anyone'), ('followers', 'Followers'), ('friends', 'Friends')])
    blocked_users_button = StringField('Blocked Users cannot view your profile or send you messages', render_kw={'type': 'button', 'value': 'Blocked Users'})
    
    
class ReportPostForm(FlaskForm):
    hateful = BooleanField('Hateful or Abusive Content')
    spam = BooleanField('Spam or Misleading')
    violence = BooleanField('Violence')
    explicit = BooleanField('Explicit Content')
    other = BooleanField('Other')
    
    def send_report(self, other_data):
        
        isHateful = self.hateful.data
        isSpan = self.spam.data
        isViolent = self.violence.data
        isExplicit = self.explicit.data
        otherBool = self.other.data
        
        print({
            "isHateful": isHateful,
            "isSpan": isSpan,
            "isViolent": isViolent,
            "isExplicit": isExplicit,
            "otherBool": otherBool,
            "other_data": other_data,
        })
        
    
class AdminUserSettings(FlaskForm):
    # user access
    canPost = BooleanField('Post Content')
    
    # user type
    isModerator = BooleanField('Has Administrator Access')
    isArtist = BooleanField('Artist Account')
    
    # user operations (ban/delete account)
    deleteUser = SubmitField('Delete User')
    