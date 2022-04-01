from main import app
from fastapi.encoders import jsonable_encoder
from fastapi import status, HTTPException, Depends
from app.sprinkler.models_schema import Sprinkler
from app.db.db_config import SessionLocal, engine
from app.sprinkler import models_table, models_query as q, models_schema
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

models_table.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/sprinkler/get-all-sprinklers')
async def get_all_sprinklers(db: Session = Depends(get_db)):
    """Returns all created sprinklers"""
    return q.get_all_sprinklers(db)


@app.put('/sprinkler/set-water-flow/{sprinkler_id}')
async def set_water_flow(sprinkler_id: int, water_flow: int, status_code=status.HTTP_200_OK,
                         db: Session = Depends(get_db)):
    """Sets the water flow from a specific sprinkler"""
    try:
        return q.set_water_flow(sprinkler_id=sprinkler_id, water_flow=water_flow, db=db)
    except NoResultFound:
        raise HTTPException(status_code=500, detail="Sprinkler not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error when searching for sprinkler: {e}")


@app.get('/sprinkler/get-sprinkler-config/{sprinkler_id}')
async def get_sprinkler_config(sprinkler_id: int, status_code=status.HTTP_200_OK, db: Session = Depends(get_db)):
    """Returns the data from a sprinkler"""
    try:
        data = q.get_sprinkler_config(db, sprinkler_id)
        return data
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Sprinkler not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error when searching for sprinkler: {e}")


@app.post('/sprinkler/create-sprinkler/{sprinkler_id}')
async def create_sprinkler(new_sprinkler: models_schema.Sprinkler, status_code=status.HTTP_201_CREATED,
                           db: Session = Depends(get_db)):
    """Creates a sprinkler"""
    try:
        sprinkler = q.add_sprinkler(db, sprinkler=new_sprinkler)
        return sprinkler
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error when creating sprinkler: {e}")


@app.delete('/sprinkler/delete-sprinkler/{sprinkler_id}', status_code=status.HTTP_200_OK)
async def delete_plant(sprinkler_id: int, db: Session = Depends(get_db)):
    """Deletes a sprinkler by id"""
    try:
        q.delete_sprinkler_by_id(db, sprinkler_id=sprinkler_id)
    except NoResultFound:
        raise HTTPException(status_code=500, detail="Sprinkler not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error when searching for sprinkler: {e}")


@app.post('/sprinkler/add-plant-sprinkler/{sprinkler_id}&{plant_id}')
async def add_plant_sprinkler(sprinkler_id: int, plant_id: int, status_code=status.HTTP_201_CREATED,
                              db: Session = Depends(get_db)):
    """Adds a plant to a sprinkler area"""
    try:
        sprinkler = q.add_plant_in_sprinkler_area(db=db, plant_id=plant_id, sprinkler_id=sprinkler_id)
        return sprinkler
    except NoResultFound:
        raise HTTPException(status_code=500, detail="Sprinkler not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error when adding plant to sprinkler area: {e}")


@app.get('/sprinkler/get-all-plants-sprinkler/{sprinkler_id}')
async def get_all_plants_in_sprinkler_area(sprinkler_id: int, status_code=status.HTTP_200_OK,
                                           db: Session = Depends(get_db)):
    """Returns all plants added on the sprinkler's area"""
    try:
        data = q.get_all_plants_in_sprinkler_area(db, sprinkler_id)
        return data
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Sprinkler not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error when searching for sprinkler: {e}")
