# blueprints/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Please enter your name."),
        Length(min=2, max=50, message="Name must be between 2 and 50 characters."),
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Please enter your email address."),
        Email(message="Please enter a valid email address."),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter a password."),
        Length(min=6, message="Password must be at least 6 characters."),
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Sign Up')