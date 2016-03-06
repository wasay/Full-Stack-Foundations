from . import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, engine, Shelters, Puppies, Owners, PuppyOwners, ShelterPuppies

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

SHELTERS = session.query(Shelters).order_by('name')