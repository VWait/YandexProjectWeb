import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Achievement(SqlAlchemyBase):
    __tablename__ = 'achievements'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    u_a1 = orm.relation("User_Achievement", backref='achievement')