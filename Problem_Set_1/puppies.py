import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    current_occupancy = Column(Integer, default=0)
    maximum_capacity = Column(Integer, default=0)


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    weight = Column(Numeric(3))
    description = Column(String)
    special_needs = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)


class Adoptors(Base):
    __tablename__ = 'adoptors'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class PuppyAdoptors(Base):
    __tablename__ = 'puppy_adoptors'
    id = Column(Integer, primary_key=True)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship(Puppy)
    adoptor_id = Column(Integer, ForeignKey('adoptors.id'))
    adoptors = relationship(Adoptors)


class ShelterPuppies(Base):
    __tablename__ = 'shelter_puppies'
    id = Column(Integer, primary_key=True)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship(Puppy)


# Create an engine that stores data in the local directory's
# puppyshelter.db file.
engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)

# print "=============================================="
# print "Puppies class file loaded"
# print "=============================================="
