from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from database_setup import Base, engine, Owners
# from flask.ext.sqlalchemy import SQLAlchemy

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

male_names = ["Noah A", "Liam B", "Mason C", "Jacob C"]

female_names = ['Emma A', 'Olivia B', 'Sophia C', 'Isabella D']

#owners = Table('owners', meta, autoload=True)
try:

    for i, x in enumerate(male_names):
        owner = Owners(id=None, name=x)
        session.add(owner)
        session.commit()

    for i, x in enumerate(female_names):
        owner = Owners(id=None, name=x)
        session.add(owner)
        session.commit()

except:
    session.rollback()
    raise
