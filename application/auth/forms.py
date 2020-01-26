from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, PasswordField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username", [validators.required(message="Please enter your name.")])
    password = PasswordField("Password", [validators.required("Please enter your password.")])
  
    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    name = StringField("Name", [validators.required(), validators.Length(
        min=2, max=50, message="Name must be between 2 and 50 characters."),
        validators.Regexp('^[a-zA-Z]+$', message="Name can contain only letters.")])
    
    username = StringField("Username", [validators.required(), validators.Length(
        min=4, max=50, message="Username must be between 4 and 30 characters."),
        validators.Regexp('^[\w]+$', message="Username can only contain alphanumeric characters.")])
    
    password = PasswordField("Password", [validators.required(), validators.Length(
        min=2, max=60, message="Password must be between 8 and 60 characters."), 
        validators.Regexp('^[\w]+$', message="Password must contain both letters and numbers.")
        ])
  
    class Meta:
        csrf = False

class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', [validators.required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')

    class Meta:
        csrf = False