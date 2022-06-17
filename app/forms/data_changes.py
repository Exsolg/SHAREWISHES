from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email
from wtforms.fields.datetime import DateField


class DataForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = DateField('Day of birth', validators=[DataRequired()], format='%d.%m.%Y')
    description = StringField('Description')
    submit = SubmitField('Submit')