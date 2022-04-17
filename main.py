from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from data import db_session
from data import hall_item
from data.users import User
from data.tables import Table
from data.halls import Hall
from data.items import Item
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
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    ###
    hall1 = db_sess.query(Hall).filter(Hall.id == 1).first()
    hall2 = db_sess.query(Hall).filter(Hall.id == 2).first()
    item1 = db_sess.query(Item).filter(Item.id == 1).first()
    item2 = db_sess.query(Item).filter(Item.id == 2).first()
    db_sess.delete(hall2)
    db_sess.delete(hall1)
    db_sess.delete(item2)
    db_sess.delete(item1)
    db_sess.commit()
    ###
    if db_sess.query(Hall).all() == [] or db_sess.query(Item).all() == []:
        hall_item.add()
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
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
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
@login_required
def map():
    db_sess = db_session.create_session()
    halls = db_sess.query(Hall).all()
    items = db_sess.query(Item).all()
    hall = {hall.id: ([i. id for i in db_sess.query(Item).filter(Item.halls_id == hall.id).all()]) for hall in halls}
    print(halls)
    return render_template("map.html", halls=halls, hall=hall, items=items, title='Map')


def main():
    db_session.global_init("db/base.sqlite")

    app.run()


if __name__ == '__main__':
    main()