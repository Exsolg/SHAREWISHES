from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired
from wtforms.fields.datetime import DateField


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat the password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    nick = StringField('Nickname', validators=[DataRequired()])
    age = DateField('Day of birth', validators=[DataRequired()], format='%d.%m.%Y')
    description = StringField('Description')
    submit = SubmitField('Submit')