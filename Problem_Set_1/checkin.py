import os
import argparse
import decimal as import_decimal
import datetime as import_datetime

from decimal import Decimal
from datetime import date
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from puppies import Shelter, Base, Puppy, ShelterPuppies, engine

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


def checkin_puppy(add_puppy_name, add_shelter_name):

    is_valid_add = 0
    is_accepting = 0
    add_shelter_id = 0
    add_puppy_id = 0

    print ''

    try:
        print ('Locating puppy named %r') % (add_puppy_name)
        print ('------------------------------------------------')
        print ('')

        puppy = session.query(Puppy.id, Puppy.name).\
            filter(Puppy.name == add_puppy_name)

        if (puppy.count() != 0):

            add_puppy_id = puppy[0].id
            add_puppy_name = puppy[0].name

        if (add_puppy_id != 0):

            print ('Is %r already Checked-In to a shelter') % (add_puppy_name)
            print ('------------------------------------------------')
            print ('')

            found_puppy = session.query(ShelterPuppies.id).\
                filter(ShelterPuppies.puppy_id == add_puppy_id)

            if (found_puppy.count() != 0):
                print ('Yes, %s is already Checked-In') % (add_puppy_name)
                add_puppy_id = 0
            else:
                print ('Yes, %s is not checked into '
                       'a shelter yet') % (add_puppy_name)

            print ('------------------------------------------------')
            print ('')

        else:

            print ('Could not locate puppy named %r') % (add_puppy_name)
            print ('------------------------------------------------')
            print ('')

            print ('Suggested list of five puppy names:')
            print ('------------------------------------------------')

            puppies_list = session.query(Puppy.name).\
                filter(Puppy.name != add_puppy_name).\
                order_by(Puppy.name).limit(5)
            print ('Suggested puppies count %s') % (puppies_list.count())

            for row in puppies_list:

                print (row.name)

        print ('------------------------------------------------')
        print ('')
    except:
        raise

    if (add_puppy_id != 0):

        try:
            print ('Locating shelter named %r') % (add_shelter_name)
            print ('------------------------------------------------')
            print ('')

            shelter = session.query(Shelter.id, Shelter.name,
                                    Shelter.current_occupancy,
                                    Shelter.maximum_capacity).\
                filter(Shelter.name == add_shelter_name)

            if (shelter.count() != 0):
                add_shelter_id = shelters[0].id
                add_shelter_name = shelters[0].name
                if (shelter[0].current_occupancy <
                   shelter[0].maximum_capacity):
                    is_accepting = 1

            if (shelter.count() == 0 or is_accepting == 0):
                if (shelter.count() == 0):
                    print ('Unable to locate %r') % (add_shelter_name)
                else:
                    print ('%r is at max capacity') % (add_shelter_name)

                print ('------------------------------------------------')
                print ('')

                print ('Locating new shelter for this puppy')
                print ('------------------------------------------------')
                print ('')

                new_shelter = session.query(Shelter.id, Shelter.name).\
                    filter(Shelter.name !=
                           add_shelter_name and
                           Shelter.current_occupancy <
                           Shelter.maximum_capacity).\
                    order_by(Shelter.maximum_capacity)

                if (new_shelter is not None and new_shelter.count() != 0):

                    add_shelter_id = new_shelter[0].id
                    add_shelter_name = new_shelter[0].name
                    is_valid_add = 1
                    print ('Found shelter %s') % (add_shelter_name)

                else:

                    print ('All shelters are at max capacity')
                    print ('Please add a new shelter for puppies')

                print ('------------------------------------------------')
                print ('')

            else:
                is_valid_add = 1

        except:
            raise

    if (is_valid_add == 1):
        try:
            add = ShelterPuppies(id=None,
                                 shelter_id=add_shelter_id,
                                 puppy_id=add_puppy_id)
            session.add(add)
            session.commit()

            print ('%r is checked in at %s') % (add_puppy, add_shelter)
            print ('------------------------------------------------')
            print ('')

            update = Shelter(id=add_shelter_id,
                             current_occupancy=current_occupancy+1)
            session.add(update)
            session.commit()

            print ('Updated current_occupancy of shelter %s') % (add_shelter)
            print ('------------------------------------------------')
            print ('')

        except:
            session.rollback()
            raise

try:
    dispatch = {
        'checkin': checkin_puppy
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('arguments', nargs='*')
    args = parser.parse_args()

    dispatch['checkin'](*args.arguments)

except:
    # raise
    print ('')
    print ('Usage:')
    print ('------------------------------------------------')
    print ('python checkin.py <puppy_name> <shelter_name>')
    print ('python checkin.py Zoey "Oakland Animal Services"')
    print ('------------------------------------------------')
    print ('')
