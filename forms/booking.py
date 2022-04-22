from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class BookingForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired()])
    phoneNumber = IntegerField('PhoneNumber', validators=[DataRequired()])
    submit = SubmitField('Забронировать')