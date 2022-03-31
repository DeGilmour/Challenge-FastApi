from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from app.plants import models_schema, models_table


def get_plant(db: Session, plant_id: int):
    # plant = db.query(models_table.Plant).filter(models_table.Plant.id == plant_id).first()
    plant = db.query(models_table.Plant).get(plant_id)
    if plant:
        return plant
    raise NoResultFound


def add_plant(db: Session, plant: models_schema.Plant):
    new_plant = models_table.Plant(**plant.dict())
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    return new_plant.to_json()


def get_all_plants(db: Session):
    return db.query(models_table.Plant).all()


def delete_plant_by_id(db: Session, plant_id: int):
    plant_to_del = get_plant(db, plant_id)
    db.delete(plant_to_del)
    db.commit()


def update_plant_by_id(db: Session, plant_id: int, plant: models_schema.Plant):
    plant_to_upt = get_plant(db, plant_id)
    print(plant.plant_name)
    for var, value in vars(plant).items():
        setattr(plant_to_upt, var, value) if value else None
    db.add(plant_to_upt)
    db.commit()
    db.refresh(plant_to_upt)
    return plant_to_upt.to_json()
