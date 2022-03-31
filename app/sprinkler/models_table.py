from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from app.db import db_config

Base = db_config.Base


class Sprinkler(db_config.Base):
    __tablename__ = "sprinkler"

    id = Column(Integer, primary_key=True, index=True)
    sprinkler_name = Column(String, unique=True, index=True)
    water_flow = Column(Integer, default=0)
    problems = Column(Boolean, default=False)
    plants_in_sprinkler_area = Column(JSON(), ForeignKey('plants.id'), nullable=True)

    def to_json(self):
        return {
            "water_flow": self.water_flow,
            "sprinkler_name": self.sprinkler_name,
            "problems": self.problems,
            "plants_in_sprinkler_area": self.plants_in_sprinkler_area
        }

# class SprinklerPlants(db_config.Base):
#     """Table stores plants a certain sprinkler area"""
#     __tablename__ = 'sprinkler_plants'

#     sprinkler = relationship('Sprinkler', foreign_keys='sprinkler.id')
#     weapon_Concealment = Column(PickleType(), ForeignKey('plant.id'), nullable=False)

# def add_column(engine, table_name, column):
#     column_name = 'plants_in_sprinkler_cover_area'
#     column_type = column.type.compile(engine.dialect)
#     engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

# del Sprinkler.__mapper__._props["plants_in_sprinkler_cover_area"]
# column = Column(PickleType(), ForeignKey('plants.id'), nullable=True)
# add_column(db_config.engine, 'sprinkler', column)
# Sprinkler.__table__.drop(db_config.engine)
