from sqlalchemy import Column, Integer, String, Text, ForeignKey
from db.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class Place(SqlAlchemyBase):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    position = Column(String)
    category_id = Column(Integer, ForeignKey('place_categories.id'), nullable=False)

    category = relationship("PlaceCategory", back_populates="places")
    events = relationship("Event", back_populates="place")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'place_cat_id': self.place_cat_id
        }
