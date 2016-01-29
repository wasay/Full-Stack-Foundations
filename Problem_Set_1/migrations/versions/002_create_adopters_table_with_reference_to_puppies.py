from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    adoptors = Table('adoptors', meta,
        Column('id', INTEGER, primary_key=True, nullable=False),
        Column('name', VARCHAR(length=250), nullable=False)
    )
    puppy_adoptors = Table('puppy_adoptors', meta,
        Column('id', INTEGER, primary_key=True, nullable=False),
        Column(Integer, ForeignKey('puppy.id')),
        Column(Integer, ForeignKey('adoptors.id'))
    )
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    puppy_adoptors = Table('puppy_adoptors', meta, autoload=True)
    puppy_adoptors.drop())
    adoptors = Table('adoptors', meta, autoload=True)
    adoptors.drop()
    pass
