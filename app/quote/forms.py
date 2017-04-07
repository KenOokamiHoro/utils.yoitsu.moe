from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class AddQuoteForm(FlaskForm):
    content = TextAreaField('内容', validators=[Required()])
    author = StringField('作者')
    source = StringField('来源')
    link = StringField('链接')
    comment = TextAreaField('备注')
   
    submit = SubmitField('OK 😋')

class MassQuoteForm(FlaskForm):
    file = FileField('JSON Here~', validators=[Required()])
    submit = SubmitField('OK 😋')