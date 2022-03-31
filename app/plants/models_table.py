from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import db_config

Base = db_config.Base


class Plant(db_config.Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    plant_name = Column(String, unique=True, index=True)
    healthy = Column(Boolean, default=True)
    type = Column(String, nullable=True)

    def to_json(self):
        return {'plant_name': self.plant_name, 'healthy': self.healthy, 'type': self.type}
