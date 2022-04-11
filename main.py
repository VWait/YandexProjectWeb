from flask import Flask, render_template
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abyfkmysqghjtrn'


@app.route("/")
def index():
    return render_template("base.html")


def main():
    db_session.global_init('db/base.sqlite')
    app.run()


if __name__ == '__main__':
    main()
