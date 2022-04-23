import os
import datetime
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
    if current_user.is_authenticated:
        return logout()
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/shelf")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    cuckoo()
    return render_template("index.html", user=current_user.is_authenticated, title='Work log')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/registration', methods=['GET', 'POST'])
def reqister():
    db_sess = db_session.create_session()
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


@app.route('/map')
def map():
    day = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг',
           4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье', 7: 'Понедельник',
           8: 'Вторник', 9: 'Среда', 10: 'Четверг', 11: 'Пятница',
           12: 'Суббота', 13: 'Воскресенье'}
    day_now = datetime.datetime.timetuple(datetime.datetime.now())
    today = day[day_now[6]] + ' ' + str(day_now[2]) + '.' + str(day_now[1]) + ' (сегодня)'
    return redirect(url_for('map_1', today=today))



@app.route('/map_1/<today>/', methods=['GET'])
def map_1(today):
    db_sess = db_session.create_session()
    items = [db_sess.query(Maps).filter(Maps.hull_number == 1).all(),
             db_sess.query(Maps).filter(Maps.hull_number == 2).all()]
    type_items = db_sess.query(Items).all()
    days = [i.type for i in db_sess.query(Days).all()]
    tables = [i.map_id for i in db_sess.query(Table).filter(Table.day_id == days.index(today) + 1).all()]
    types = {}
    for i in type_items:
        types[i.id] = i.type
    for i in range(len(items)):
        for j in range(len(items[i])):
            if items[i][j].id in tables:
                items[i][j] = ['Забронировано', items[i][j].id]
            elif types[items[i][j].item_id] == 'Стол' or types[items[i][j].item_id] == 'PS4':
                form = BookingForm()
                form.map_id = items[i][j].id
                form.submit.label.text = f'Забронировать стол №{items[i][j].id}'
                items[i][j] = [types[items[i][j].item_id], form]
            else:
                items[i][j] = [types[items[i][j].item_id], items[i][j].id]
    surname = request.args.get('surname')
    number = request.args.get('number')
    submit = request.args.get('submit')
    if surname:
        submit = int(submit.split('№')[1])
        table = Table(
            surname=surname,
            number=number,
            day_id=days.index(today) + 1,
            use_id=current_user.id,
            map_id=submit
        )
        db_sess.add(table)
        db_sess.commit()
        return redirect(url_for('map_1', today=today))
    return render_template("map.html", items=items, days=days, today=today, title='Map')


@app.route('/shelf')
def shelf():
    db_sess = db_session.create_session()
    games = db_sess.query(Games).all()
    return render_template("shelf.html", games=games, title='Shelf')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    db_sess = db_session.create_session()
    if request.method == 'GET':
        user_achievement = db_sess.query(User_Achievement).filter(User_Achievement.user_id == current_user.id).all()
        achievement_id = [i.achiev_id for i in user_achievement]
        achievement = [i.id for i in db_sess.query(Achievement).filter().all()]
        achievements = [db_sess.query(Achievement).filter(Achievement.id == i).first() for i in achievement if
                        i in achievement_id]

        tables = [[i.map_id, db_sess.query(Days).filter(Days.id == i.day_id).first().type]
                  for i in db_sess.query(Table).filter(Table.use_id == current_user.id).all()]
        return render_template("profile.html", tables=tables, user=current_user, achievements=achievements, title='Profile')
    elif request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(os.path.dirname(__file__), 'static/img', file.filename))
            FILE = os.path.join('static/img', file.filename)
            print(FILE)
            user = User(id=current_user.id,img=FILE)
            db_sess.merge(user)
            db_sess.commit()
        return redirect(url_for('profile'))


def cuckoo():
    db_sess = db_session.create_session()
    day = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг',
           4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье', 7: 'Понедельник',
           8: 'Вторник', 9: 'Среда', 10: 'Четверг', 11: 'Пятница',
           12: 'Суббота', 13: 'Воскресенье'}
    today = {'Понедельник': [1, ''], 'Вторник': [2, ''], 'Среда': [3, ''], 'Четверг': [4, ''],
             'Пятница': [5, ''], 'Суббота': [6, ''], 'Воскресенье': [7, '']}
    dt = datetime.datetime.now()
    day_now = datetime.datetime.timetuple(dt)
    if day_now[6] == 0:
        last_day = 7
    else:
        last_day = day_now[6]
    today[day[day_now[6]]][1] = day[day_now[6]] + ' ' + str(day_now[2]) + '.' + str(day_now[1]) + ' (сегодня)'
    today[day[day_now[6] + 1]][1] = day[day_now[6] + 1] + ' ' + str(day_now[2] + 1) + '.' + str(day_now[1]) + ' (завтра)'
    today[day[day_now[6] + 2]][1] = day[day_now[6] + 2] + ' ' + str(day_now[2] + 2) + '.' + str(day_now[1])
    today[day[day_now[6] + 3]][1] = day[day_now[6] + 3] + ' ' + str(day_now[2] + 3) + '.' + str(day_now[1])
    today[day[day_now[6] + 4]][1] = day[day_now[6] + 4] + ' ' + str(day_now[2] + 4) + '.' + str(day_now[1])
    today[day[day_now[6] + 5]][1] = day[day_now[6] + 5] + ' ' + str(day_now[2] + 5) + '.' + str(day_now[1])
    today[day[day_now[6] + 6]][1] = day[day_now[6] + 6] + ' ' + str(day_now[2] + 6) + '.' + str(day_now[1])

    for table in db_sess.query(Table).filter(Table.day_id == last_day).all():
        db_sess.delete(table)

    for i in today:
        day_week = Days(id=today[i][0],
                        type=today[i][1])
        db_sess.merge(day_week)
    db_sess.commit()
    return day, day_now


def main():
    db_session.global_init("db/base.sqlite")

    app.run()


if __name__ == '__main__':
    main()