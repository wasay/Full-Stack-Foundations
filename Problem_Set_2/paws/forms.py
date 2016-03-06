from . import app, data

from flask.ext.wtf import Form

from wtforms import BooleanField, StringField, validators
from wtforms import DateField, DateTimeField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError


class PuppyForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=250)])
    gender = SelectField(u'Gender', choices=[('', 'Select'), ('female', 'Female'), ('male', 'Male')])
    #dateOfBirth  = DateField('Birthday', format='%%y-%%m-%%d')
    dateOfBirth  = StringField('Birthday')
    picture = StringField('Picture', [validators.Length(min=4, max=250)])
    weight = StringField('Weight', [validators.Length(min=1, max=5)])
    shelter_id = SelectField('Shelter', coerce=int)