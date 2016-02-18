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
from puppies import Adoptors, PuppyAdoptors

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


def adopt_a_puppy(puppy_ids, adopter_name):

    print ''

    try:

        #print ('Puppy IDs: %s') % (puppy_ids)
        #print ''

        for id in puppy_ids:
            is_valid_adopt = 0
            add_puppy_id = 0
            shelter_id = 0

            # print ('id: %s') % (id)
            # print ''

            puppy = session.query(Puppy.id, Puppy.name).\
                filter(Puppy.id == id)

            print ('Puppy id %s found = %s') % (id, puppy.count())
            print ('------------------------------------------------')
            print ('')

            if (puppy.count() != 0):

                add_puppy_id = puppy[0].id
                add_puppy_name = puppy[0].name

            if (add_puppy_id != 0):

                print ('Is %s with id %s already adopted?') % (add_puppy_name, add_puppy_id)
                print ('------------------------------------------------')
                print ('')

                found_puppy = session.query(PuppyAdoptors.id).\
                    filter(PuppyAdoptors.puppy_id == add_puppy_id)

                if (found_puppy.count() != 0):
                    print ('Yes, %s is already adopted') % (add_puppy_name)
                    add_puppy_id = 0

                else:
                    print ('No, %s is not adopted yet') % (add_puppy_name)

                    print ('Locating adopter named %r') % (adopter_name)
                    print ('------------------------------------------------')
                    print ('')

                    adopter = session.query(Adoptors.id, Adoptors.name).\
                        filter(Adoptors.name == adopter_name)

                    if (adopter.count() == 0):
                        print ('Unable to locate adoptor %r') % (adopter_name)
                    else:
                        is_valid_adopt = 1
                        add_adopter_id = adopter[0].id
                        add_adopter_name = adopter[0].name


            if (is_valid_adopt == 1):
                try:
                    # record puppy adoptors
                    add = PuppyAdoptors(id=None,
                                         adoptor_id=add_adopter_id,
                                         puppy_id=add_puppy_id)
                    session.add(add)
                    session.commit()
                    print ('%r is adopted by %s') % (add_puppy_name, add_adopter_name)
                    print ('------------------------------------------------')
                    print ('')

                    # find puppy record from shelter puppies
                    shelter_puppies = session.query(ShelterPuppies.id, ShelterPuppies.shelter_id).\
                        filter(ShelterPuppies.puppy_id == add_puppy_id)

                    if (shelter_puppies.count() != 0):

                        # record shelter id
                        shelter_id = shelter_puppies[0].shelter_id

                        # remove puppy record from shelter puppies
                        session.query(ShelterPuppies.id, ShelterPuppies.shelter_id).\
                        filter(ShelterPuppies.puppy_id == add_puppy_id).delete()

                    # find puppy shelter
                    puppy_shelter = session.query(Shelter.name,
                                          Shelter.current_occupancy).\
                        filter(Shelter.id == shelter_id)

                    if (puppy_shelter.count() > 0):

                        shelter_name = puppy_shelter[0].name
                        shelter_occupancy = puppy_shelter[0].current_occupancy

                        # update shelter occupancy: current_occupancy -1
                        session.query(Shelter.id).\
                            filter(Shelter.id == shelter_id).\
                            update({Shelter.current_occupancy: shelter_occupancy-1},
                        synchronize_session=False)
                        session.commit()


                except:
                    session.rollback()
                    raise
            print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
            print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'

        print ('------------------------------------------------')
        print ('')
    except:
        raise

    print ''

try:
    dispatch = {
        'adopt': adopt_a_puppy
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('arguments', nargs='*')
    args = parser.parse_args()

    dispatch['adopt'](*args.arguments)

except:
    raise
    print ('')
    print ('Usage:')
    print ('------------------------------------------------')
    print ('python adopt.py <puppy_ids> <adopter_name>')
    print ('python adopt.py "2,4" "Emma A"')
    print ('python adopt.py "2,4" "Noah A"')
    print ('------------------------------------------------')
    print ('')
