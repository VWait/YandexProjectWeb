import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Table(SqlAlchemyBase):
    __tablename__ = 'tables'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_table = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    nickname = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, unique=True)

    datetime = sqlalchemy.Column(sqlalchemy.DateTime,
                                 default=datetime.datetime.now())
    users = orm.relation('User')

