from fastapi import FastAPI
from sqlalchemy.orm import Session

from app import logger
from app import models
from app.db import SessionLocal
from app.db import engine
from app.exception import NotFoundException, InternalServerException

"""
So that FastAPI knows that it has to treat a variable as a dependency, we will import Depends
"""
from fastapi import Depends

# import crud to give access to the operations that we defined
from app import crud

# initialize FastApi instance
app = FastAPI()

# create the database tables on app startup or reload
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    """ This function is used to get db connection """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# define endpoint
@app.post("/create_address")
def create_address(location: str, latitude: float, longitude: float, db: Session = Depends(get_db)):
    """

    :param location: Name of the city/town
    :param latitude: latitude of the location
    :param longitude: longitude of the location
    :return: Newly created address
    """
    try:
        address = crud.create_address(db=db, location=location, latitude=latitude, longitude=longitude)
        # return object created
        logger.logging.info('Address created successfully')
        return {"address": address, 'Message': 'Address created successfully', 'status code': 200}
    except InternalServerException as e:
        logger.logging.error('Log Error Message')
        return {'Error': 'Something went wrong', 'status code': 400}


@app.put("/update_address/{id}/")  # id is a path parameter
def update_address(id: int, location: str, latitude: float, longitude: float, db: Session = Depends(get_db)):
    """
    :param id: address id from the database
    :param location: Name of the city/town
    :param latitude: latitude of the location
    :param longitude: longitude of the location
    :return: Updated address
    """
    # get address object from database
    db_address = crud.get_address(db=db, id=id)
    # check if address object exists
    try:
        if db_address:
            updated_address = crud.update_address(db=db, id=id, location=location, latitude=latitude,
                                                  longitude=longitude)
            logger.logging.info('Address updated successfully')
            return {"updated_address": updated_address, 'Message': 'Address updated successfully', 'status code': 200}
    except NotFoundException:
        logger.logging.error('Log Error Message')
        return {"error": f"Address with id {id} does not exist", 'status code': 400}


@app.delete("/delete_address/{id}/")  # id is a path parameter
def delete_address(id: int, db: Session = Depends(get_db)):
    """

    :param id: address id from the database
    :return: Successfully deleted message
    """
    # get address object from database
    db_address = crud.get_address(db=db, id=id)
    # check if address object exists
    try:
        if db_address:
            crud.delete_address(db=db, id=id)
            logger.logging.info('Address deleted successfully')
            return {"message": f"Address with id {id} has been deleted", 'status code': 200}
    except NotFoundException:
        logger.logging.error('Log Error Message')
        return {"error": f"Address with id {id} does not exist", 'status code': 400}


@app.get("/list_all_addresses")
def list_all_addresses(db: Session = Depends(get_db)):
    """
    Def: get all the addresses in the address book
    Params:
    Returns: List of all the addresses from the address book
    """
    try:
        address_list = crud.list_addresses(db=db)
        logger.logging.info('Addresses displayed successfully')
        return {'Addresses': address_list, 'status code': 200}
    except InternalServerException:
        logger.logging.error('Log Error Message')
        return {'Error': 'Something went wrong', 'status code': 400}


@app.get("/list_by_coordinates")
def list_by_coordinates(start_lat: float, end_lat: float, start_long: float, end_long: float,
                        db: Session = Depends(get_db)):
    """

    :param start_lat: the starting latitude in the range
    :param end_lat: the ending latitude in the range
    :param start_long: the starting longitude in the range
    :param end_long: the ending longitude in the range
    :return: list of addresses with the given range
    """
    try:
        address_list = crud.get_address_by_coordinates(db=db, start_lat=start_lat, end_lat=end_lat, start_long=start_long,
                                                       end_long=end_long)
        logger.logging.info('Addresses displayed successfully')
        return {'Addresses': address_list, 'status code': 200}
    except InternalServerException:
        logger.logging.error('Log Error Message')
        return {'Error': 'Something went wrong', 'status code': 400}


@app.get("/list_by_distance")
def list_by_distance(target_address_id: int, distance_radius_from_target: int, db: Session = Depends(get_db)):
    """

    :param target_address_id: address id from the database
    :param distance_radius_from_target: distance in kilometers
    :return: list of addresses with the given range
    """
    try:
        address_list = crud.get_addresses_in_given_distance(db=db, target_address_id=target_address_id,
                                                            distance_radius_from_target=distance_radius_from_target)
        logger.logging.info('Addresses displayed successfully')
        return {'Addresses': address_list, 'status code': 200}
    except InternalServerException:
        logger.logging.error('Log Error Message')
        return {'Error': 'Something went wrong', 'status code': 400}