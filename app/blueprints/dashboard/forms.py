# blueprints/dashboard/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateDeckForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message="Please enter a title for the deck."),
        Length(min=3, max=100, message="Title must be between 3 and 100 characters."),
    ])
    submit = SubmitField('Create')
