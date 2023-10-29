from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):# naming this type methos is very important here
        user = User.query.filter(User.username == username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists ! please try a different username')
    def validate_email_address(self, email_to_check):
        email = User.query.filter(User.email_address == email_to_check.data).first()
        if email:
            raise ValidationError('Email address already exists ! please try a different Email address')
    username = StringField(label='Username:', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address:',validators=[Email(),DataRequired()])
    password1 = StringField(label='Password:', validators=[Length(min=6),DataRequired()])
    password2 = StringField(label='Confirm Password:', validators=[EqualTo('password1'),DataRequired()])

    submit= SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username',validators=[DataRequired()])
    password = StringField(label='Password:',validators=[DataRequired()])
    submit= SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    submit= SubmitField(label='Purchase Item!')


class SellItemForm(FlaskForm):
    submit= SubmitField(label='Sell Item!')




