import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User_Achievement(SqlAlchemyBase):
    __tablename__ = 'user_achiev'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    achiev_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("achievements.id"))

    user = orm.relation('User')
    achievement = orm.relation('Achievement')
