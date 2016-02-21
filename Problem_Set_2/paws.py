from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, engine, Shelters, Puppies, Owners, PuppyOwners, ShelterPuppies
from flask.ext.sqlalchemy import Pagination
import datetime

app = Flask(__name__)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

PER_PAGE = 20

@app.route('/')
@app.route('/puppies')
@app.route('/puppies/')
@app.route('/puppies/page')
@app.route('/puppies/page/')
@app.route('/puppies/<int:page>/')
@app.route('/puppies/page/<int:page>/')
def showPuppies(page=1):

    all_results = session.query(Puppies).order_by('name')
    all_count = all_results.count()

    if page == 1:
        results = session.query(Puppies).order_by('name').limit(PER_PAGE)
    else:
        results = session.query(Puppies).order_by('name').limit(PER_PAGE).offset(PER_PAGE*(page-1))

    if not results and page != 1:
        abort(404)
    pagination = Pagination(all_results, page, PER_PAGE, all_count, None)

    endpoint = 'showPuppies'

    return render_template('puppies.html', results=results, all_count=all_count, endpoint=endpoint, pagination=pagination)

@app.route('/puppy/new', methods=['GET', 'POST'])
def newPuppy():
    if request.method == 'POST':
        if request.form['name']:

            name = request.form['name']
            gender = request.form['gender']
            dateOfBirth = request.form['dateOfBirth']
            picture = request.form['picture']
            weight = request.form['weight']
            shelter_id = request.form['shelter_id']

            day,month,year = dateOfBirth.split('/')
            dateOfBirth = datetime.date(int(year),int(month),int(day))

            newItem = Puppies(name=name,
                gender=gender,
                dateOfBirth=dateOfBirth,
                picture=picture,
                weight=weight,
                shelter_id=shelter_id)

            session.add(newItem)
            session.commit()
            flash("New Puppy Created")
        else:
            flash("New Puppy Not Created")
        return redirect(url_for('showPuppies'))
    else:
        return render_template('newpuppy.html')

@app.route('/puppy/<int:puppy_id>/edit', methods=['GET', 'POST'])
def editPuppy(puppy_id):

    puppy = session.query(Puppies).filter_by(id=puppy_id).one()

    if request.method == 'POST':
        if request.form['name']:
            puppy.name = request.form['name']
            session.add(puppy)
            session.commit()
            flash("Puppy Successfully Edited")
        else:
            flash("Puppy Not Edited")
        return redirect(url_for('showPuppies'))
    else:
        return render_template(
            'editpuppy.html', puppy_id=puppy_id, item=puppy)

@app.route('/puppy/<int:puppy_id>/delete', methods=['GET', 'POST'])
def deletePuppy(puppy_id):

    puppy = session.query(Puppies).filter_by(id=puppy_id).one()

    if puppy :

        if request.method == 'POST':
            session.delete(puppy)
            session.commit()
            flash("Puppy Successfully Deleted")
            return redirect(url_for('showPuppies'))
        else:
            return render_template(
                'deletepuppy.html', item=puppy)
    else:
        flash("Unable to locate Puppy")
        return redirect(url_for('showPuppies'))

@app.route('/shelters')
@app.route('/shelters/')
@app.route('/shelters/page')
@app.route('/shelters/page/')
@app.route('/shelters/<int:page>/')
@app.route('/shelters/page/<int:page>/')
def showShelters(page=1):

    all_results = session.query(Shelters).order_by('name')
    all_count = all_results.count()

    if page == 1:
        results = session.query(Shelters).order_by('name').limit(PER_PAGE)
    else:
        results = session.query(Shelters).order_by('name').limit(PER_PAGE).offset(PER_PAGE*(page-1))

    if not results and page != 1:
        abort(404)
    pagination = Pagination(all_results, page, PER_PAGE, all_count, None)

    endpoint = 'showShelters'

    return render_template('shelters.html', results=results, all_count=all_count, endpoint=endpoint, pagination=pagination)


@app.route('/shelter/new', methods=['GET', 'POST'])
def newShelter():
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            zipCode = request.form['zipCode']
            website = request.form['website']
            maximum_capacity = request.form['maximum_capacity']

            newItem = Shelters(name=name,
                address=address,
                city=city,
                state=state,
                zipCode=zipCode,
                website=website,
                maximum_capacity=maximum_capacity)

            session.add(newItem)
            session.commit()
            flash("New Shelter Created")
        else:
            flash("New Shelter Not Created")

        return redirect(url_for('showShelters'))
    else:
        return render_template('newshelter.html')

@app.route('/shelter/<int:shelter_id>/edit', methods=['GET', 'POST'])
def editShelter(shelter_id):

    shelter = session.query(Shelters).filter_by(id=shelter_id).one()

    if request.method == 'POST':
        if request.form['name']:
            shelter.name = request.form['name']
            shelter.address = request.form['address']
            shelter.city = request.form['city']
            shelter.state = request.form['state']
            shelter.zipCode = request.form['zipCode']
            shelter.website = request.form['website']
            shelter.maximum_capacity = request.form['maximum_capacity']

            session.add(shelter)
            session.commit()
            flash("Shelter Successfully Edited")
        else:
            flash("Shelter Not Edited")
        return redirect(url_for('showShelters'))
    else:
        return render_template(
            'editshelter.html', shelter_id=shelter_id, item=shelter)

@app.route('/shelter/<int:shelter_id>/delete', methods=['GET', 'POST'])
def deleteShelter(shelter_id):

    shelter = session.query(Shelters).filter_by(id=shelter_id).one()

    if shelter :

        if request.method == 'POST':
            session.delete(shelter)
            session.commit()
            flash("Shelter Successfully Deleted")
            return redirect(url_for('showShelters'))
        else:
            return render_template(
                'deleteshelter.html', item=shelter)
    else:
        flash("Unable to locate Shelter")
        return redirect(url_for('showShelters'))

@app.route('/owners')
@app.route('/owners/')
@app.route('/owners/page')
@app.route('/owners/page/')
@app.route('/owners/<int:page>/')
@app.route('/owners/page/<int:page>/')
def showOwners(page=1):

    all_results = session.query(Owners).order_by('name')
    all_count = all_results.count()

    if page == 1:
        results = session.query(Owners).order_by('name').limit(PER_PAGE)
    else:
        results = session.query(Owners).order_by('name').limit(PER_PAGE).offset(PER_PAGE*(page-1))

    if not results and page != 1:
        abort(404)
    pagination = Pagination(all_results, page, PER_PAGE, all_count, None)

    endpoint = 'showOwners'

    return render_template('owners.html', results=results, all_count=all_count, endpoint=endpoint, pagination=pagination)


@app.route('/owner/new', methods=['GET', 'POST'])
def newOwner():
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']

            newItem = Owners(name=name)

            session.add(newItem)
            session.commit()
            flash("New Owner Created")
        else:
            flash("New Owner Not Created")

        return redirect(url_for('showOwners'))
    else:
        return render_template('newowner.html')

@app.route('/owner/<int:owner_id>/edit', methods=['GET', 'POST'])
def editOwner(owner_id):
    return render_template('editowner.html')

@app.route('/owner/<int:owner_id>/delete', methods=['GET', 'POST'])
def deleteOwner(owner_id):
    return render_template('deleteowner.html')

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)