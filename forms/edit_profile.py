from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField
from wtforms.validators import DataRequired


class EditForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    new_password = PasswordField('Password', validators=[DataRequired()])
    new_password_again = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Изменить')
