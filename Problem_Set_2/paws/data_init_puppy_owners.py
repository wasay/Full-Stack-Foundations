from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from models import Base, engine, Puppies, Owners, PuppyOwners
# from flask.ext.sqlalchemy import SQLAlchemy

from random import randint
import random

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

try:
    puppies_list = session.query(Puppies.id, Puppies.name).order_by(Puppies.name).limit(9)
    for row in puppies_list:
        puppy_adopt = PuppyOwners(id=None, puppy_id=row.id,
                                    owner_id=randint(1, 8))
        session.add(puppy_adopt)

        row.shelter_id=None
        session.add(row)

        session.commit()
except:
    session.rollback()
    raise
