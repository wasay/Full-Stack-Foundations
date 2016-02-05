import os
import decimal as import_decimal
import datetime as import_datetime

from datetime import date
from datetime import datetime
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy import join
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from puppies import Shelter, Base, Puppy, engine

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
    print ('Suggested list of five puppy names:')
    print ('------------------------------------------------')

    shelters = session.query(Shelter.id, Shelter.name)
    puppies = session.query(Puppy.id, Puppy.name)
    shelter_puppies = session.query(shelter_id, puppy_id)

    puppies_per_shelter = puppies.count() / shelters.count()
    puppies_per_shelter = rount(puppies_per_shelter)

    print ('Move %s puppies to unassigned shelter') % (puppies_to_add)
    remove_puppies = session.query(ShelterPuppies.id).limit(puppies_to_add)
    for row in remove_puppies:
        puppy_remove = ShelterPuppies(id=row.id)
        session.delete(puppy_remove)
        session.commit()

    for row in shelters:
        print ('Update max capacity for %s to %s') % (row.name, puppies_per_shelter)
        print ('------------------------------------------------')

        shelter = Shelter(id=row.id, max_capacity_update=puppies_per_shelter)
        if (shelter is not None):
            session.update(shelter)
            session.commit()

        print (' for %s to %s') % (row.name, puppies_per_shelter)
        print ('------------------------------------------------')
        puppies_per_shelter = session.query(ShelterPuppies.shelter_id,
            ShelterPuppies.puppy_id).filter(shelter_id==row.id)
        puppies_to_add = puppies_per_shelter - puppies_per_shelter.count()

        if (puppies_to_add > 0):
            print ('Add puppies to this shelter')
            add_puppies = session.query(Puppy).join(ShelterPuppies,
                Puppy.c.id != ShelterPuppies.c.puppy_id)
            add_puppies = puppies.join(address_table,
                user_table.c.id == address_table.c.user_id)

except:
    session.rollback()
    raise
