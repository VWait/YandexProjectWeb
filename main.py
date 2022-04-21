import os
import datetime
import schedule
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data import add
from data.users import User
from data.games import Games
from data.items import Items
from data.maps import Maps
from data.days import Days
from data.table import Table
from data.achievements import Achievement
from data.user_achiev import User_Achievement
from flask_login import UserMixin
from forms.login_form import LoginForm
from forms.register import RegisterForm
from forms.edit_form import EditForm
from forms.booking import BookingForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abyfkmysqghjtrn'


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    print(db_sess.query(Games).all())
    #add.add_2()
    if db_sess.query(Achievement).all() == []:
        add.add_1()
    if db_sess.query(Games).all() == []:
        add.add()
    users = db_sess.query(User).all()
    names = {name.id: (name.nickname) for name in users}
    cuckoo()
    return render_template("index.html", names=names, title='Work log')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/registration', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter((User.email == form.email.data) | (User.nickname == form.nickname.data)).first():
            return render_template('register.html', title='Register', form=form,
                                   message="Этот пользователь уже зарегистрирован")
        user = User(
            nickname=form.nickname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    db_sess = db_session.create_session()
    form = BookingForm()
    if form.validate_on_submit():
        if len(str(form.number.data)) != 11:
            return render_template('booking.html', message="Неправильно набран номер", form=form)
        table = Table(
            surname=form.surname.data,
            number=form.number.data
        )
        db_sess.add(table)
        db_sess.commit()
        return redirect("/")
    return render_template('booking.html', form=form)


@app.route('/map')
def map():
    db_sess = db_session.create_session()
    items = [db_sess.query(Maps).filter(Maps.hull_number == 1).all(), db_sess.query(Maps).filter(Maps.hull_number == 2).all()]
    type_items = db_sess.query(Items).all()
    types = {}
    for i in type_items:
        types[i.id] = i.type
    print(types)
    return render_template("map.html", items=items, types=types, title='Map')


@app.route('/shelf')
def shelf():
    db_sess = db_session.create_session()
    games = db_sess.query(Games).all()
    print(games[0].img)
    return render_template("shelf.html", games=games, title='Shelf')


@app.route('/profile',)
@login_required
def profile():
    db_sess = db_session.create_session()
    user_achievement = db_sess.query(User_Achievement).filter(User_Achievement.user_id == current_user.id).all()
    achievement_id = [i.achiev_id for i in user_achievement]
    achievement = [i.id for i in db_sess.query(Achievement).filter().all()]
    achievements = [db_sess.query(Achievement).filter(Achievement.id == i).first() for i in achievement if i in achievement_id]
    return render_template("profile.html", user=current_user, achievements=achievements, title='Profile')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    db_sess = db_session.create_session()
    form = EditForm()
    form.nickname.data = current_user.nickname
    form.email.data = current_user.email
    if form.validate_on_submit():
        print(11111111111111111111)
        user = User(
            nickname=form.nickname.data,
            email=form.email.data
        )
        if form.new_password.data != '' and form.new_password_again.data != '':
            if form.new_password.data != form.new_password_again.data:
                return render_template('edit_profile.html', title='Edition', form=form,
                                       message="Новые пароли не совпадают")
            if form.password.data != current_user.password:
                return render_template('edit_profile.html', title='Edition ', form=form,
                                        message="Неправильный пароль")
            user.set_password(form.password.data)
        db_sess.merge(user)
        db_sess.commit()
        return redirect('/profile')
    return render_template("edit_profile.html", message="Неправильный пароль1", form=form, user=current_user, title='Edit_profile')


def cuckoo():
    db_sess = db_session.create_session()
    day = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг',
           4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье', 7: 'Понедельник',
           8: 'Вторник', 9: 'Среда', 10: 'Четверг', 11: 'Пятница',
           12: 'Суббота', 13: 'Воскресенье'}
    today = {'Понедельник': '', 'Вторник': '', 'Среда': '', 'Четверг': '',
             'Пятница': '', 'Суббота': '', 'Воскресенье': ''}
    dt = datetime.datetime.now()
    day_now = datetime.datetime.timetuple(dt)
    today[day[day_now[6]]] = day[day_now[6]] + ' ' + str(day_now[2]) + '.' + str(day_now[1]) + ' (сегодня)'
    today[day[day_now[6] + 1]] = day[day_now[6] + 1] + ' ' + str(day_now[2] + 1) + '.' + str(day_now[1]) + ' (завтра)'
    today[day[day_now[6] + 2]] = day[day_now[6] + 2] + ' ' + str(day_now[2] + 2) + '.' + str(day_now[1])
    today[day[day_now[6] + 3]] = day[day_now[6] + 3] + ' ' + str(day_now[2] + 3) + '.' + str(day_now[1])
    today[day[day_now[6] + 4]] = day[day_now[6] + 4] + ' ' + str(day_now[2] + 4) + '.' + str(day_now[1])
    today[day[day_now[6] + 5]] = day[day_now[6] + 5] + ' ' + str(day_now[2] + 5) + '.' + str(day_now[1])
    today[day[day_now[6] + 6]] = day[day_now[6] + 6] + ' ' + str(day_now[2] + 6) + '.' + str(day_now[1])

    for i in db_sess.query(Days).all():
        db_sess.delete(i)

    for i in today:
        day_week = Days(type=today[i])
        db_sess.add(day_week)
    db_sess.commit()


def main():
    db_session.global_init("db/base.sqlite")

    app.run()


if __name__ == '__main__':
    main()