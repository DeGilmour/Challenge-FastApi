from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from app.sprinkler import models_schema, models_table
from app.plants.models_query import get_plant
import json


def get_sprinkler_config(db: Session, sprinkler_id: int):
    spr = db.query(models_table.Sprinkler).get(sprinkler_id)
    if spr:
        return spr
    raise NoResultFound


def add_sprinkler(db: Session, sprinkler: models_schema.Sprinkler) -> dict:
    new_spr = models_table.Sprinkler(**sprinkler.dict())
    db.add(new_spr)
    db.commit()
    db.refresh(new_spr)
    return new_spr.to_json()


def get_all_sprinklers(db: Session) -> models_table.Sprinkler:
    return db.query(models_table.Sprinkler).all()


def delete_sprinkler_by_id(db: Session, sprinkler_id: int):
    spr_to_del = get_sprinkler_config(db, sprinkler_id)
    db.delete(spr_to_del)
    db.commit()


def set_water_flow(db: Session, sprinkler_id: int, water_flow: int) -> dict:
    upt_sprinkler = get_sprinkler_config(db, sprinkler_id)
    upt_sprinkler.water_flow = water_flow
    db.add(upt_sprinkler)
    db.commit()
    db.refresh(upt_sprinkler)
    return upt_sprinkler.to_json()


# def add_plant_in_sprinkler_area(db: Session, plant_id: int, sprinkler_id: int) -> dict:
#     sprinkler = get_sprinkler_config(db, sprinkler_id)
#     if sprinkler.plants_in_sprinkler_area:
#         sprinkler.plants_in_sprinkler_area = json.loads(sprinkler.plants_in_sprinkler_area)
#     else:
#         sprinkler.plants_in_sprinkler_area = []
#     if sprinkler.plants_in_sprinkler_area:
#         plant = get_plant(db, plant_id=plant_id)
#         if not plant:
#             raise NoResultFound
#         if plant_id not in sprinkler.plants_in_sprinkler_area:
#             sprinkler.plants_in_sprinkler_area.append(plant_id)
#             new_list = sprinkler.plants_in_sprinkler_area
#         else:
#             raise Exception("Plant already in sprinkler area")
#     else:
#         sprinkler.plants_in_sprinkler_area = [plant_id]
#         new_list = sprinkler.plants_in_sprinkler_area
#     sprinkler.plants_in_sprinkler_area = json.dumps(new_list)
#     db.add(sprinkler)
#     db.commit()
#     db.refresh(sprinkler)
#     return sprinkler.to_json()

def add_plant_in_sprinkler_area(db: Session, plant_id: int, sprinkler_id: int) -> dict:
    sprinkler = get_sprinkler_config(db, sprinkler_id)
    plant = get_plant(db, plant_id)
    new_plant_in_sprinkler_area = models_table.PlantsInSprinkler(plant=plant.id, sprinkler=sprinkler.id)
    db.add(new_plant_in_sprinkler_area)
    db.commit()
    db.refresh(new_plant_in_sprinkler_area)
    return new_plant_in_sprinkler_area.to_json()


# def get_all_plants_in_sprinkler_area(db: Session, sprinkler_id: int) -> list:
#     sprinkler = get_sprinkler_config(db=db, sprinkler_id=sprinkler_id).to_json()
#     plants = []
#     if sprinkler['plants_in_sprinkler_area']:
#         plants = json.loads(sprinkler['plants_in_sprinkler_area'])
#     list_plants = []
#     for id in plants:
#         plant_obj = get_plant(db, plant_id=id)
#         list_plants.append(plant_obj)
#     return list_plants

def get_all_plants_in_sprinkler_area(db: Session, sprinkler_id: int) -> list:
    sprinkler = get_sprinkler_config(db=db, sprinkler_id=sprinkler_id)
    plants_in_sprinkler_area = db.query(models_table.PlantsInSprinkler).filter(
        models_table.PlantsInSprinkler.sprinkler == sprinkler.id).all()
    return plants_in_sprinkler_area
