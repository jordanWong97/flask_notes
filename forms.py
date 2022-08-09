"""forms for app"""


from flask_wtf import FlaskForm
# import your own form types and validators
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email, Length
import email_validator


class CreateUserForm(FlaskForm):
    """Form for creating users."""

    username = StringField('Username', validators=[InputRequired(),
                                                   Length(max=20)])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(max=100)])
    email = EmailField('Email', validators=[InputRequired(),
                                            Email(),
                                            Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(),
                                                       Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(),
                                                     Length(max=30)])


class LoginForm(FlaskForm):
    """Form for creating users."""

    username = StringField('Username', validators=[InputRequired(),
                                                   Length(max=20)])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(max=100)])
