from sqlalchemy import Column, Integer, String, ForeignKey
from db.db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship


class PlaceCategory(SqlAlchemyBase):
    __tablename__ = 'place_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    parent_id = Column(Integer, ForeignKey("place_categories.id"))
    parent = relationship("PlaceCategory", remote_side=[id])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent": self.parent.to_dict() if self.parent_id is not None else None
        }
