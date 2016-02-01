from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    shelter = Table('shelter', meta, autoload=True)

    col1 = Column('current_occupancy', Integer)
    col1.create(shelter)

    col2 = Column('maximum_capacity', Integer)
    col2.create(shelter)
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    shelter = Table('shelter', meta, autoload=True)

    shelter.c.current_occupancy.drop()
    shelter.c.maximum_capacity.drop()
    pass
