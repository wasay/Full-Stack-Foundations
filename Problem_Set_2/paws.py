from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy, Owners, PuppyOwners, ShelterPuppies, engine
from flask.ext.sqlalchemy import Pagination

app = Flask(__name__)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

PER_PAGE = 20

@app.route('/')
@app.route('/puppies')
@app.route('/puppies/<int:page>/')
@app.route('/puppies/page')
@app.route('/puppies/page/<int:page>/')
def showPuppies(page):

    all_puppies = session.query(Puppy).order_by('name')
    all_count = all_puppies.count()

    if page == 1:
        puppies = session.query(Puppy).order_by('name').limit(PER_PAGE)
    else:
        puppies = session.query(Puppy).order_by('name').limit(PER_PAGE).offset(PER_PAGE*(page-1))

    if not puppies and page != 1:
        abort(404)
    pagination = Pagination(all_puppies, page, PER_PAGE, all_count, None)

    endpoint = 'showPuppies'

    return render_template('puppies.html', puppies=puppies, all_count=all_count, endpoint=endpoint, pagination=pagination)

@app.route('/puppy/new', methods=['GET', 'POST'])
def newPuppy():
    return "Add Puppy Information"

@app.route('/puppy/<int:puppy_id>/edit', methods=['GET', 'POST'])
def editPuppy(puppy_id):
    return "Edit Puppy Information"

@app.route('/puppy/<int:puppy_id>/delete', methods=['GET', 'POST'])
def deletePuppy(puppy_id):
    return "Delete Puppy Information"

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)