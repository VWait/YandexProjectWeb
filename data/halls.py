import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Hall(SqlAlchemyBase):
    __tablename__ = 'halls'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    top = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    left = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    width = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    height = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    items = orm.relation("Item", back_populates='hall')