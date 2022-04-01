from main import app
from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.plants import models_table, models_query as q, models_schema
from app.db.db_config import SessionLocal, engine
from sqlalchemy.orm.exc import NoResultFound

models_table.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/plants/{plant_id}')
async def get_plant_by_plant_id(plant_id: int, db: Session = Depends(get_db)):
    """Returns a specific plant by id"""
    try:
        plant = q.get_plant(db, plant_id=plant_id)
        return plant.to_json()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Plant not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error when getting plant: {e}")


@app.get('/all-plants')
async def get_all_plants(db: Session = Depends(get_db)):
    """Returns all plants"""
    return q.get_all_plants(db)


@app.post('/plants/create-plant/{plant_id}')
async def create_plant(new_plant: models_schema.Plant, status_code=status.HTTP_201_CREATED,
                       db: Session = Depends(get_db)):
    """Creates a plant"""
    try:
        new_plant = q.add_plant(db, plant=new_plant)
        return new_plant
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error when creating plant: {e}")


@app.put('/plants/update-plant{plant_id}')
async def update_plant(plant_id: int, plant: models_schema.Plant, db: Session = Depends(get_db)):
    """Updates the content of the plant table"""
    return q.update_plant_by_id(db, plant_id=plant_id, plant=plant)


@app.delete('/plants/delete-plant/{plant_id}', status_code=status.HTTP_200_OK)
async def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    """Deletes a plant by id"""
    try:
        q.delete_plant_by_id(db, plant_id=plant_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Plant not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error when creating plant: {e}")
