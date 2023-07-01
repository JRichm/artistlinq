""" ### Server Imports ### """

from flask import Flask, render_template, redirect, url_for
import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'


""" ### Flask Routes ### """

    ### " View Homepage " ###
    
@app.route('/')
def index():
    return render_template('index.html')
  
  
    ### " View Login/New User" ###
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = forms.LoginForm()
    newUserForm = forms.RegistrationForm()
    if loginForm.validate_on_submit() or newUserForm.validate_on_submit():
        # Process login form submission
        print('fart')
        # Perform authentication and redirect
        return redirect(url_for('index'))
    return render_template('login.html', loginForm=loginForm, newUserForm=newUserForm)


""" ### Server Methods ### """

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)