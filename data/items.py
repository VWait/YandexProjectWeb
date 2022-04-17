import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Item(SqlAlchemyBase):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    halls_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("halls.id"))
    top = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    left = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    width = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    height = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    hall = orm.relation('Hall')
