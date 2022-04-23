from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class BookingForm(FlaskForm):
    map = IntegerField("Map_id", validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    number = IntegerField('PhoneNumber', validators=[DataRequired()])
    submit = SubmitField('Забронировать')