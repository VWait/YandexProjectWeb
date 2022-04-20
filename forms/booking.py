from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class BookingForm(FlaskForm):
    name_table = StringField("Table name", validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    number = IntegerField('Phone number', validators=[DataRequired()])
    datetime = DateTimeField('Game time', validators=[DataRequired()])
    submit = SubmitField('Забронировать')
