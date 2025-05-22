from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class Event(SqlAlchemyBase):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    datetime = Column(DateTime)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('event_categories.id'), nullable=False)

    place = relationship("Place", back_populates="events")
    category = relationship("EventCategory", back_populates="events")
