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
    image_url = Column(String)

    category = relationship("PlaceCategory")
    events = relationship("Event")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'position': self.position,
            'category': {
                'category_id': self.category_id,
                'category_name': self.category.name,
                'category_parent_id': self.category.parent_id
            },
            'image_url': self.image_url
        }
