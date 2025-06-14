from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class Event(SqlAlchemyBase):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    datetime = Column(DateTime)
    image_url = Column(String)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('event_categories.id'), nullable=False)

    place = relationship("Place")
    category = relationship("EventCategory")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'datetime': self.datetime,
            'image_url': self.image_url,
            'place_id': self.place_id,
            'category': {
                'category_id': self.category_id,
                'category_name': self.category.name,
                'category_parent_id': self.category.parent_id
            }
        }
