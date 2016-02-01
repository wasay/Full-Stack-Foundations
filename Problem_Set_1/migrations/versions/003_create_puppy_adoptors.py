from sqlalchemy import *
from migrate import *
from migrate.changeset.constraint import ForeignKeyConstraint

meta = MetaData()

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine

    puppy_adoptors = Table('puppy_adoptors', meta,
        Column('id', INTEGER, primary_key=True, nullable=False),
        Column('puppy_id', INTEGER),
        Column('adoptor_id', Integer)
    )
    puppy_adoptors.create()

    puppy = Table('puppy', meta, autoload=True)
    adoptors = Table('adoptors', meta, autoload=True)
    puppy_adoptors = Table('puppy_adoptors', meta, autoload=True)

    cons1 = ForeignKeyConstraint([puppy_adoptors.c.puppy_id], [puppy.c.id])
    cons1.create()

    cons2 = ForeignKeyConstraint([puppy_adoptors.c.adoptor_id], [adoptors.c.id])
    cons2.create()
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine

    puppy = Table('puppy', meta, autoload=True)
    adoptors = Table('adoptors', meta, autoload=True)
    puppy_adoptors = Table('puppy_adoptors', meta, autoload=True)

    cons1 = ForeignKeyConstraint([puppy_adoptors.c.puppy_id], [puppy.c.id])
    cons1.drop()

    cons2 = ForeignKeyConstraint([puppy_adoptors.c.adoptor_id], [adoptors.c.id])
    cons2.drop()

    puppy_adoptors.drop()
    pass
