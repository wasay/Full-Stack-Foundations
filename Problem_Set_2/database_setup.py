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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipCode': self.zipCode,
            'website': self.website,
            'current_occupancy': self.current_occupancy,
            'maximum_capacity': self.maximum_capacity,
        }


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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'dateOfBirth': self.dateOfBirth,
            'picture': self.picture,
            'weight': self.weight,
            'description': self.description,
            'special_needs': self.special_needs,
            'shelter_id': self.shelter_id,
        }


class Owners(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class PuppyOwners(Base):
    __tablename__ = 'puppy_adoptors'
    id = Column(Integer, primary_key=True)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship(Puppy)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    owners = relationship(Owners)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'puppy_id': self.puppy_id,
            'owner_id': self.owner_id,
        }


class ShelterPuppies(Base):
    __tablename__ = 'shelter_puppies'
    id = Column(Integer, primary_key=True)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship(Puppy)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'shelter_id': self.shelter_id,
            'puppy_id': self.puppy_id,
        }

engine = create_engine('sqlite:///puppyshelter.db')


Base.metadata.create_all(engine)