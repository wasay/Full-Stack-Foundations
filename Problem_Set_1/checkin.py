import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import argparse

import decimal as import_decimal
from decimal import Decimal

Base = declarative_base()

from puppies import Shelter, Base, Puppy, ShelterPuppies, engine

import datetime as import_datetime
from datetime import date
from datetime import datetime


# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

def checkin(puppy_name, shelter_name):

    shelters = session.query(Shelter.id, Shelter.name,
                           Shelter.current_occupancy,
                           Shelter.maximum_capacity).\
                       filter(Shelter.name == shelter_name)
    shelter_count = shelters.count()

    shelter_accepting = 0
    req_shelter_id = 0
    if (shelter_count != 0):
        req_shelter_id = shelters[0].id
        if (shelters[0].current_occupancy < shelters[0].maximum_capacity):
            shelter_accepting = 1

    puppies = session.query(Puppy.id, Puppy.name).\
                      filter(Puppy.name == puppy_name)
    puppy_count = puppies.count()
    req_puppy_id = 0
    if (puppy_count != 0):
        req_puppy_id = puppies[0].id


    if (shelter_count == 0 or shelter_accepting == 0):
        if (shelter_count == 0):
            print ('Could not locate the shelter named %r') % (shelter_name)
        else:
            print ('This shelter is not accepting any new puppies')

        print ''
        print ('Additional shelters:')
        for row in session.query(Shelter.id, Shelter.name).\
                           filter(Shelter.name != shelter_name and
                                  Shelter.current_occupancy < Shelter.maximum_capacity).\
                           order_by(Shelter.name):
            print (row.name)
    elif (puppy_count == 0):
        print ('Could not locate puppy named %r') % (puppy_name)
        print ''
        print ('Additional puppies:')
        for row in session.query(Puppy.name).\
                           filter(Puppy.name != puppy_name).\
                           order_by(Puppy.name):
            print (row.name)

        print ''
    else:

        shelter_puppies = session.query(ShelterPuppies.id).\
                          filter(ShelterPuppies.puppy_id == req_puppy_id)
        if (shelter_puppies.count() == 0):
            print ('Shelter ID: %s and Puppy ID: %s') % (req_shelter_id, req_puppy_id)
            try:
                shelter_puppy = ShelterPuppies(id=None,
                                               shelter_id = req_shelter_id,
                                               puppy_id = req_puppy_id)
                session.add(shelter_puppy)
                session.commit()
            except:
                session.rollback()
                raise
            print ('The puppy %r is checked in at shelter %s') % (puppy_name, shelter_name)
        else:
            print ('The puppy is already checked in to a shelter')


dispatch = {
    'checkin': checkin
}

try:
    parser = argparse.ArgumentParser()
    parser.add_argument('function')
    parser.add_argument('arguments', nargs='*')
    args = parser.parse_args()

    dispatch[args.function](*args.arguments)

#check if requested shelter has capacity for one
# if no, check if any shelter has capacity for one
	# if no, prompt user to create a new shelter
	# if yes, add puppy to shelter
# if yes, add puppy to shelter

except:
   session.rollback()
   raise