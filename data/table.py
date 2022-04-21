import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Table(SqlAlchemyBase):
    __tablename__ = 'table'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    use_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    day_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("days.id"))
    map_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("maps.id"))

    day = orm.relation('Days')
    map = orm.relation('Maps')
    user = orm.relation('User')