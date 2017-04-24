from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField,SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class OsuUserForm(FlaskForm):
    username = StringField('用户名？', validators=[Required()])
    mode = SelectField('模式？',validators=[Required()])
    submit = SubmitField('OK 😋')

    def __init__(self, *args, **kwargs):
        super(OsuUserForm, self).__init__(*args, **kwargs)
        self.mode.choices = [(1,"Standard"),
                             (2,"Taiko"),
                             (3,"osu!Catch"),
                             (4,"osu!mania")]
        

class MassQuoteForm(FlaskForm):
    file = FileField('JSON Here~', validators=[Required()])
    submit = SubmitField('OK 😋')