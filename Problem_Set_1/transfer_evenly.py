import os
import decimal as import_decimal
import datetime as import_datetime

from datetime import date
from datetime import datetime
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy import join
from sqlalchemy import update
from sqlalchemy.orm import query
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from puppies import Shelter, Base, Puppy, engine, ShelterPuppies

Base = declarative_base()

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

try:

    shelters = session.query(Shelter.id, Shelter.name,
                             Shelter.current_occupancy)
    puppies = session.query(Puppy.id, Puppy.name)

    puppies_per_shelter_count = puppies.count() / shelters.count()
    puppies_per_shelter_count = round(puppies_per_shelter_count)

    session.query(ShelterPuppies).delete()

    session.query(Shelter).\
        update({Shelter.current_occupancy: 0,
                Shelter.maximum_capacity: puppies_per_shelter_count},
               synchronize_session=False)
    session.commit()

    for puppy in puppies:

        accepting_shelter = session.query(Shelter.id, Shelter.name,
                                          Shelter.current_occupancy).\
            filter(Shelter.current_occupancy < puppies_per_shelter_count).\
            limit(1)

        if (accepting_shelter.count() > 0):

            shelter_id = accepting_shelter[0].id
            shelter_name = accepting_shelter[0].name
            shelter_occupancy = accepting_shelter[0].current_occupancy

            add = ShelterPuppies(id=None,
                                 shelter_id=shelter_id,
                                 puppy_id=puppy.id)
            session.add(add)
            session.commit()

            session.query(Shelter.id).filter(Shelter.id == shelter_id).\
                update({Shelter.current_occupancy: shelter_occupancy+1},
                       synchronize_session=False)
            session.commit()

except:
    session.rollback()
    raise
