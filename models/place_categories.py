from sqlalchemy import Column, Integer, String, ForeignKey
from db.db_session import SqlAlchemyBase


class PlaceCategory(SqlAlchemyBase):
    __tablename__ = 'place_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    parent_id = Column(Integer, ForeignKey("place_categories.id"))
