import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Map(SqlAlchemyBase):
    __tablename__ = 'map'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("items.id"))
    hull_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pos_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    item = orm.relation("Items")
