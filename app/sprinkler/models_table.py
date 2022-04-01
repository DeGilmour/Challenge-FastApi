from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from app.db import db_config
from app.plants.models_table import Plant

Base = db_config.Base


class Sprinkler(db_config.Base):
    __tablename__ = "sprinkler"

    id = Column(Integer, primary_key=True, index=True)
    sprinkler_name = Column(String, unique=True, index=True)
    water_flow = Column(Integer, default=0)
    problems = Column(Boolean, default=False)

    def to_json(self):
        return {
            "water_flow": self.water_flow,
            "sprinkler_name": self.sprinkler_name,
            "problems": self.problems
        }


class PlantsInSprinkler(db_config.Base):
    __tablename__ = "plants_in_sprinkler"

    id = Column(Integer, primary_key=True, index=True)
    sprinkler = Column(Integer, ForeignKey(Sprinkler.id))
    plant = Column(Integer, ForeignKey(Plant.id))

    def to_json(self):
        return {
            "id": self.id,
            "sprinkler": self.sprinkler,
            "plant": self.plant
        }
