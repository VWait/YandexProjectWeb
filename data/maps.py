import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Maps(SqlAlchemyBase):
    __tablename__ = 'maps'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("items.id"))
    hull_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pos_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    closed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    item = orm.relation("Items")
    map = orm.relation("Table", back_populates='map')
