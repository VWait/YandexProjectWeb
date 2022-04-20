import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Items(SqlAlchemyBase):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    items = orm.relation("Maps", back_populates='item')