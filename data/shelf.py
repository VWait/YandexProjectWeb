import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Shelf(SqlAlchemyBase):
    __tablename__ = 'shelf'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)