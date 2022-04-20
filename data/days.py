import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Days(SqlAlchemyBase):
    __tablename__ = 'days'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    days = orm.relation("Table", back_populates='day')