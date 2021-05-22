# auth/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(3,20, message='Please enter a username of 3 - 20 characters')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Enter Password', validators=[DataRequired(), Length(8), EqualTo('confirm', message='Password does not match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
