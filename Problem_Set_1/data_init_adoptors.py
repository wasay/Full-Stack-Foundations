from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppies import Shelter, Base, Puppy, Adoptors, engine
# from flask.ext.sqlalchemy import SQLAlchemy


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

male_names = ["Noah A", "Liam B", "Mason C", "Jacob C"]

female_names = ['Emma A', 'Olivia B', 'Sophia C', 'Isabella D']

adoptors = Table('adoptors', meta, autoload=True)
try:

    for i, x in enumerate(male_names):
        adoptor = Adoptors(id=None, name=x)
        session.add(adoptor)
        session.commit()

    for i, x in enumerate(female_names):
        adoptor = Adoptors(id=None, name=x)
        session.add(adoptor)
        session.commit()

except:
    session.rollback()
    raise
