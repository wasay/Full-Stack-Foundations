from sqlalchemy import *
from migrate import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

male_names = ["Noah A", "Liam B", "Mason C", "Jacob C"]
female_names = ['Emma A', 'Olivia B', 'Sophia C', 'Isabella D']

Base = declarative_base()
engine = create_engine('sqlite:///puppyshelter.db')
meta = MetaData(bind=engine)
DBSession = sessionmaker(bind=engine)
# session.rollback()
session = DBSession()

class Adoptors(Base):
    __table__ = Table('adoptors', meta, autoload=True)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)

    adoptors = Table('adoptors', meta, autoload=True)

    for i, x in enumerate(male_names):
	  adoptor = Adoptors(id=None, name=x)
	  session.add(adoptor)
	  session.commit()

    for i, x in enumerate(female_names):
	  adoptor = Adoptors(id=None, name=x)
	  session.add(adoptor)
	  session.commit()
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    adoptors = Table('adoptors', meta, autoload=True)

    for i, x in enumerate(male_names):
        adoptor = adoptors.filter(name=x)
        adoptors.drop(adoptor)

    for i, x in enumerate(female_names):
        adoptor = adoptors.filter(name=x)
        adoptors.drop(adoptor)
    pass
