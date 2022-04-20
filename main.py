from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data import add
from data.users import User
from data.games import Games
from data.tables import Table
from data.achievements import Achievement
from data.user_achiev import User_Achievement
from flask_login import UserMixin
from forms.booking import BookingForm
from forms.login_form import LoginForm
from forms.register import RegisterForm

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
    #db_sess.delete(db_sess.query(Achievement).filter(Achievement.id == 1).first())
    #db_sess.commit()
    #add.add_2()
    if db_sess.query(Achievement).all() == []:
        add.add_1()
    users = db_sess.query(User).all()
    names = {name.id: (name.nickname) for name in users}
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
        db_sess = db_session.create_session()
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
    form = BookingForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template('booking.html', message="Booking", form=form)


@app.route('/map')
def map():
    db_sess = db_session.create_session()
    return render_template("map.html", title='Map')


@app.route('/shelf')
def shelf():
    db_sess = db_session.create_session()
    games = db_sess.query(Games).all()
    print(games[0].img)
    return render_template("shelf.html", games=games, title='Shelf')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    db_sess = db_session.create_session()
    user_achievement = db_sess.query(User_Achievement).filter(User_Achievement.user_id == current_user.id).all()
    achievement_id = [i.achiev_id for i in user_achievement]
    achievement = [i.id for i in db_sess.query(Achievement).filter().all()]
    achievements = [db_sess.query(Achievement).filter(Achievement.id == i).first() for i in achievement if i in achievement_id]
    return render_template("profile.html", user=current_user, achievements=achievements, title='Profile')



def main():
    db_session.global_init("db/base.sqlite")

    app.run()


if __name__ == '__main__':
    main()