from . import app, data

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, engine, Shelters, Puppies, Owners, PuppyOwners, ShelterPuppies

from forms import PuppyForm
from flask import request

from flask.ext.sqlalchemy import Pagination
import datetime

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

PER_PAGE = 20

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/puppies/page/<int:page>/')
def showPuppies(page):

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

    return render_template('puppies.html', results=results, all_count=all_count,
        endpoint=endpoint, pagination=pagination)

@app.route('/puppy/new', methods=['GET', 'POST'])
def newPuppy():

    form = PuppyForm()
    form.shelter_id.choices = [(0, 'Select')]
    form.shelter_id.choices += [(shelter.id, shelter.name) for shelter in session.query(Shelters).order_by('name')]
    print form.errors



    if form.validate_on_submit():
        name = form.name.data
        gender = form.gender.data
        dateOfBirth = form.dateOfBirth.data
        picture = form.picture.data
        weight = form.weight.data
        shelter_id = form.shelter_id.data

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
        return redirect(url_for('showPuppies', page=1))
    else:
        return render_template('newpuppy.html', form=form)

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
        return redirect(url_for('showPuppies', page=1))
    else:
        shelters = session.query(Shelters).order_by('name')
        return render_template(
            'editpuppy.html', puppy_id=puppy_id, item=puppy, shelters=shelters)

@app.route('/puppy/<int:puppy_id>/delete', methods=['GET', 'POST'])
def deletePuppy(puppy_id):

    puppy = session.query(Puppies).filter_by(id=puppy_id).one()

    if puppy :

        if request.method == 'POST':
            session.delete(puppy)
            session.commit()
            flash("Puppy Successfully Deleted")
            return redirect(url_for('showPuppies', page=1))
        else:
            return render_template(
                'deletepuppy.html', item=puppy)
    else:
        flash("Unable to locate Puppy")
        return redirect(url_for('showPuppies', page=1))

@app.route('/puppy/<int:puppy_id>/view')
def viewPuppy(puppy_id):

    puppy = session.query(Puppies).filter_by(id=puppy_id).one()

    shelters = session.query(Shelters).order_by('name')
    owners = session.query(Owners).order_by('name')
    puppy_owners = session.query(PuppyOwners).filter_by(puppy_id=puppy_id)

    return render_template(
        'viewpuppy.html', puppy_id=puppy_id, item=puppy, shelters=shelters,
        owners=owners, puppy_owners=puppy_owners)

@app.route('/puppy/<int:puppy_id>/adopt', methods=['GET', 'POST'])
def adoptPuppy(puppy_id):

    puppy = session.query(Puppies).filter_by(id=puppy_id).one()

    if puppy :

        if request.method == 'POST':
            puppy_owners = session.query(PuppyOwners).filter_by(puppy_id=puppy_id)
            for puppy_owner in puppy_owners:
                session.delete(puppy_owner)
                session.commit()

            owner_ids = request.form['owner_ids']
            for owner in owner_ids:

                newItem = PuppyOwners(puppy_id=puppy_id,
                    owner_id=owner)

                session.add(newItem)

                puppy.shelter_id=None
                session.add(puppy)

                session.commit()

            flash("Puppy Successfully Adopted by Owner")
            return redirect(url_for('showPuppies', page=1))
        else:
            owners = session.query(Owners).order_by('name')
            puppy_owners = session.query(PuppyOwners)
            return render_template(
                'adoptpuppy.html', puppy_id=puppy_id, item=puppy, owners=owners, puppy_owners=puppy_owners)
    else:
        flash("Unable to locate Puppy")
        return redirect(url_for('showPuppies', page=1))


@app.route('/shelters/page/<int:page>/')
def showShelters(page):

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

@app.route('/shelter/<int:shelter_id>/checkin', methods=['GET', 'POST'])
def checkinShelter(shelter_id):

    shelter = session.query(Shelters).filter_by(id=shelter_id).one()

    if request.method == 'POST':
        if request.form['puppy_ids']:
            puppy_ids = request.form['puppy_ids']

            for puppy_id in puppy_ids:
                puppy = session.query(Puppies).filter_by(id=puppy_id).one()

                puppy_owners = session.query(PuppyOwners).filter_by(puppy_id=puppy.id)
                for puppy_owner in puppy_owners:
                    session.delete(puppy_owner)
                    session.commit()

                puppy.shelter_id = shelter_id
                session.add(puppy)
                session.commit()

            flash("Shelter Checkin Successfully Update")
        else:
            flash("Shelter Checkin Not Complete")
        return redirect(url_for('showShelters'))
    else:
        puppies = session.query(Puppies).order_by('name')

        return render_template(
            'checkinshelter.html', shelter_id=shelter_id, item=shelter, puppies=puppies)


@app.route('/shelters/evenDistribution', methods=['GET', 'POST'])
def evenlyDistributePuppiesAcrossShelters():

    if request.method == 'POST':
        try:

            shelters = session.query(Shelters.id, Shelters.name,
                                     Shelters.current_occupancy)
            puppies = session.query(Puppies.id, Puppies.name)

            puppies_per_shelter_count = puppies.count() / shelters.count()
            puppies_per_shelter_count = round(puppies_per_shelter_count)

            session.query(ShelterPuppies).delete()

            session.query(Shelters).\
                update({Shelters.current_occupancy: 0,
                        Shelters.maximum_capacity: puppies_per_shelter_count},
                       synchronize_session=False)
            session.commit()

            for puppy in puppies:

                accepting_shelter = session.query(Shelters.id, Shelters.name,
                                                  Shelters.current_occupancy).\
                    filter(Shelters.current_occupancy < puppies_per_shelter_count).\
                    limit(1)

                if (accepting_shelter.count() > 0):

                    shelter_id = accepting_shelter[0].id
                    shelter_name = accepting_shelter[0].name
                    shelter_occupancy = accepting_shelter[0].current_occupancy

                    add = ShelterPuppies(id=None,
                                         shelter_id=shelter_id,
                                         puppy_id=puppy.id)
                    session.add(add)
                    session.commit()

                    session.query(Shelters.id).filter(Shelters.id == shelter_id).\
                        update({Shelters.current_occupancy: shelter_occupancy+1},
                               synchronize_session=False)
                    session.commit()

            flash("Evenly distributed Puppies across Shelters")
            return redirect(url_for('showShelters'))

        except:
            session.rollback()
            flash("Error unable to evenly distributed Puppies across Shelters")
            return redirect(url_for('showShelters'))

    else:

        return render_template(
            'evendistributioninshelters.html')


@app.route('/owners/page/<int:page>/')
def showOwners(page):

    all_results = session.query(Owners).order_by('name')
    all_count = all_results.count()

    if page == 1:
        results = session.query(Owners).order_by('name').limit(PER_PAGE)
    else:
        results = session.query(Owners).order_by('name').limit(PER_PAGE).offset(PER_PAGE*(page-1))

    if not results and page != 1:
        # flash("Error")
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

    owner = session.query(Owners).filter_by(id=owner_id).one()

    if request.method == 'POST':
        if request.form['name']:
            owner.name = request.form['name']

            session.add(owner)
            session.commit()
            flash("Owner Successfully Edited")
        else:
            flash("Owner Not Edited")
        return redirect(url_for('showOwners'))
    else:
        return render_template(
            'editowner.html', owner_id=owner_id, item=owner)

@app.route('/owner/<int:owner_id>/delete', methods=['GET', 'POST'])
def deleteOwner(owner_id):

    owner = session.query(Owners).filter_by(id=owner_id).one()

    if owner :

        if request.method == 'POST':
            session.delete(owner)
            session.commit()
            flash("Owner Successfully Deleted")
            return redirect(url_for('showOwners'))
        else:
            return render_template(
                'deleteowner.html', item=owner)
    else:
        flash("Unable to locate Owner")
        return redirect(url_for('showOwners'))

def url_for_pagination(endpoint, page):
    page_url = ('%s, page=%s') % (endpoint, page)
    return url_for(page_url)

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['url_for_pagination'] = url_for_pagination