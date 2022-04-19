import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Games(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)