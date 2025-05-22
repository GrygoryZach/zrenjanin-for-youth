from sqlalchemy import Column, Integer, String
from db.db_session import SqlAlchemyBase


class EventCategory(SqlAlchemyBase):
    __tablename__ = 'event_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
