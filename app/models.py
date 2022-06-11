from sqlalchemy import Column, Integer, String, Float
from .db import Base


# model/table
class Address(Base):
    """
    This class is used to define a blueprint for the address_db database
    """

    __tablename__ = "address_book"

    # fields
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
