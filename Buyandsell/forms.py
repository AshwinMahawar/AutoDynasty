import email
from click import confirm
from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    name= StringField('Name', [validators.Length(min=4, max=25)])
    #username= StringField('Username', [validators.Length(min=4, max=25)])
    email= StringField('Email', [validators.Length(min=4, max=25),validators.Email()])
    password= PasswordField('New Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm=PasswordField('Repeat Password')

class LoginForm(Form):
    email= StringField('Email', [validators.Length(min=4, max=25)])
    password= PasswordField('New Password',[validators.DataRequired()])