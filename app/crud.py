from sqlalchemy.orm import Session
from . import logger
from app.models import Address
from geopy.distance import great_circle


def create_address(db: Session, location, latitude, longitude):
    """
    Function to create a Address model object
    """
    # create Address instance
    new_address = Address(location=location, latitude=latitude, longitude=longitude)
    # place object in the database session
    db.add(new_address)
    # commit your instance to the database
    db.commit()
    # refresh the attributes of the given instance
    db.refresh(new_address)
    logger.logging.info('Address created successfully')
    return new_address


def get_address(db: Session, id: int):
    """
    Gets the first record with a given id, if no such record exists, will return null
    """
    db_address = db.query(Address).filter(Address.id == id).first()
    return db_address


def update_address(db: Session, id: int, location: str, latitude: float, longitude: float):
    """
    Updates an Address object's attributes
    """
    db_address = get_address(db=db, id=id)
    db_address.location = location
    db_address.latitude = latitude
    db_address.longitude = longitude

    db.commit()
    db.refresh(db_address)  # refresh the attribute of the given instance
    return db_address


def delete_address(db: Session, id: int):
    """
    Deletes an Address object
    """
    db_address = get_address(db=db, id=id)
    db.delete(db_address)
    db.commit()  # save changes to db


def list_addresses(db: Session):
    """
    Return a list of all existing Address records
    """
    all_addresses = db.query(Address).all()
    return all_addresses


def get_address_by_coordinates(db: Session, start_lat: float, end_lat: float, start_long: float, end_long: float):
    """
    Gets all the addresses within the given co-ordinates
    """
    db_address = db.query(Address).filter(Address.latitude >= start_lat).filter(Address.latitude <= end_lat).filter(
        Address.longitude >= start_long).filter(Address.longitude <= end_long).all()
    return db_address


def get_addresses_in_given_distance(db: Session, target_address_id: int, distance_radius_from_target: int):
    """
    Gets all the addresses within the given radius from the target location
    """
    # get all the addresses
    addresses = db.query(Address).all()

    filtered_addresses = []

    target_address = db.query(Address).filter(Address.id == target_address_id).first()

    # get the coordinates of the target address and save it as a tuple
    coords_1 = (target_address.latitude, target_address.longitude)

    # loop through all the addresses to check the distance
    for address in addresses:
        # check if the address is not target address
        if address.id != target_address.id:
            coords_2 = (address.latitude, address.longitude)
            # get the distance in kms using geopy
            # check if the distance is within the limit, if yes then append the address to the filtered_address
            if (great_circle(coords_1, coords_2)) <= distance_radius_from_target:
                filtered_addresses.append(address)
    return filtered_addresses
