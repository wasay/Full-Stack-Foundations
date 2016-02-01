from sqlalchemy import *
from migrate import *

import puppies
from puppies import Base, Shelter, Puppy, Adoptors, PuppyAdoptors

male_names = ["Noah A", "Liam B", "Mason C", "Jacob C"]
female_names = ['Emma A', 'Olivia B', 'Sophia C', 'Isabella D']

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    adoptors = Table('adoptors', meta, autoload=True)

    for i, x in enumerate(male_names):
        adoptor = Adoptors(id=None, name=x)
        adoptors.add(adoptor)

    for i, x in enumerate(female_names):
        adoptor = Adoptors(id=None, name=x)
        adoptors.add(adoptor)
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
