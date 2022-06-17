from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, FileField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class WishForm(FlaskForm):
    id = IntegerField("ID")
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Upload image', validators=[FileAllowed(['jpg', 'png'], 'image only')])
    link = StringField('Link')
    description = StringField('Description', validators=[DataRequired()])
    is_private = BooleanField('Private')

    submit = SubmitField('Add')
