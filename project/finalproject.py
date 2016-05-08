from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User

import httplib2, json, requests, random, string
import pycurl, urllib, StringIO

from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response

# ######################################
# Application
# ######################################

app = Flask(__name__)

# ######################################
# Get Config settings from config files
# ######################################

# ######################################
# Amazon
# ######################################
AMZ_CLIENT_SECRETS = json.loads(
    open('instance/amz_client_secrets.json', 'r').read())['web']
AMZ_CLIENT_ID = AMZ_CLIENT_SECRETS['client_id']
AMZ_CLIENT_SECRET = AMZ_CLIENT_SECRETS['client_secret']
AMZ_APP_ID = AMZ_CLIENT_SECRETS['app_id']

# ######################################
# Facebook
# ######################################
FB_CLIENT_SECRETS = json.loads(
    open('instance/fb_client_secrets.json', 'r').read())['web']
FB_CLIENT_ID = FB_CLIENT_SECRETS['app_secret']
FB_CLIENT_SECRET = FB_CLIENT_SECRETS['app_secret']
FB_APP_ID = FB_CLIENT_SECRETS['app_id']

# ######################################
# Google
# ######################################
G_CLIENT_SECRETS = json.loads(
    open('instance/g_client_secrets.json', 'r').read())['web']
G_CLIENT_ID = G_CLIENT_SECRETS['client_id']
G_CLIENT_SECRET = G_CLIENT_SECRETS['client_secret']
G_APP_ID = G_CLIENT_SECRETS['project_id']


# ######################################
# Application Name
# ######################################
APPLICATION_NAME = "Restaurant Menu App"

# ######################################
# Database path
# ######################################
SQLALCHEMY_DATABASE_URI = 'sqlite:///restaurantmenu.db'


# Connect to Database and create database session
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# ######################################
# Show all restaurants
# ######################################
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    print 'login_session %s' % login_session
    restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
    if 'username' not in login_session:
        return render_template('publicrestaurants.html', restaurants=restaurants)
    else:
        creator = getUserInfo(login_session['user_id'])
        return render_template('restaurants.html', restaurants=restaurants, creator=creator, login_session=login_session)


# ######################################
# Create anti-forgery state token
# ######################################
def getReqState():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state


# ######################################
# Website Authentication
# ######################################

@app.route('/login')
def showLogin():
    getReqState()
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=login_session['state'], AMZ_CLIENT_ID=AMZ_CLIENT_ID, FB_APP_ID=FB_APP_ID, G_CLIENT_ID=G_CLIENT_ID)


@app.route('/logout')
def showLogout():
    getReqState()
    # return "The current session state is %s" % login_session['state']

    amzdisconnect()

    fbdisconnect()

    gdisconnect()

    showRestaurants()

# ######################################
# Amazon Authentication
# ######################################

@app.route('/amzlogin')
def showAmzLogin():
    getReqState()
    # return "The current session state is %s" % login_session['state']

    return render_template('amzlogin.html', STATE=login_session['state'], AMZ_CLIENT_ID=AMZ_CLIENT_ID)


# ######################################
# Amazon Connect
# ######################################
# Route with Method: POST
@app.route('/amzconnect', methods=['POST'])
def amzconnect():
    if request.args.get('state') != login_session['state']:
        response = 'Invalid state parameter.'
        # response = make_response(json.dumps(response), 401)
        # response.headers['Content-Type'] = 'application/json'
        # return response
        flash(response)
        return redirect(url_for('showRestaurants'))

    access_token = request.data
    print "access token received %s " % access_token

    b = StringIO.StringIO()

    # verify that the access token belongs to us
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "https://api.amazon.com/auth/o2/tokeninfo?access_token=" + urllib.quote_plus(access_token))
    c.setopt(pycurl.SSL_VERIFYPEER, 1)
    c.setopt(pycurl.WRITEFUNCTION, b.write)

    c.perform()
    d = json.loads(b.getvalue())

    stored_token = d['aud']

    if d['aud'] != AMZ_CLIENT_ID :
        # the access token does not belong to us
        # raise BaseException("Invalid Token")
        flash("Invalid Token Amazon")
        return redirect(url_for('showRestaurants'))

    # exchange the access token for user profile
    b = StringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(pycurl.URL, "https://api.amazon.com/user/profile")
    c.setopt(pycurl.HTTPHEADER, ["Authorization: bearer " + access_token])
    c.setopt(pycurl.SSL_VERIFYPEER, 1)
    c.setopt(pycurl.WRITEFUNCTION, b.write)

    c.perform()
    data = json.loads(b.getvalue())

    login_session['provider'] = 'amazon'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['amazon_id'] = data["user_id"]

    login_session['access_token'] = stored_token

    login_session['picture'] = ''

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s in Amazon" % login_session['username'])
    return redirect(url_for('showRestaurants'))

# #########################################################################
# DISCONNECT - Revoke a current user's token and reset their login_session
# #########################################################################

# ######################################
# Amazon Disconnect
# ######################################
# Route with Method: GET
@app.route('/amzdisconnect')
def amzdisconnect():
    amazon_id = login_session['amazon_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://api.amazon.com/auth/o2/tokeninfo?access_token=%s' % (amazon_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]

    flash("You have been logged out from Amazon")
    return redirect(url_for('showRestaurants'))


# ######################################
# Facebook Authentication
# ######################################
@app.route('/fblogin')
def showFbLogin():
    getReqState()
    # return "The current session state is %s" % login_session['state']
    return render_template('fblogin.html', STATE=login_session['state'], FB_APP_ID=FB_APP_ID)


# ######################################
# Facebook Connect
# ######################################
# Route with Method: POST
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s in Facebook" % login_session['username'])
    return redirect(url_for('showRestaurants'))

# #########################################################################
# DISCONNECT - Revoke a current user's token and reset their login_session
# #########################################################################

# ######################################
# Facebook Disconnect
# ######################################
# Route with Method: GET
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]

    flash("You have been logged out from Facebook")
    return redirect(url_for('showRestaurants'))


# ######################################
# Google Authentication
# ######################################
@app.route('/glogin')
def showGLogin():
    getReqState()
    # return "The current session state is %s" % login_session['state']
    return render_template('glogin.html', STATE=login_session['state'], G_CLIENT_ID=G_CLIENT_ID)


# ######################################
# Google Connect
# ######################################
# Route with Method: POST
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = 'Invalid state parameter.'
        # response = make_response(json.dumps(response), 401)
        # response.headers['Content-Type'] = 'application/json'
        flash(response)
        return redirect(url_for('glogin'))

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('instance/g_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = 'Failed to upgrade the authorization code.'
        # response = make_response(json.dumps(response), 401)
        # response.headers['Content-Type'] = 'application/json'
        flash(response)
        return redirect(url_for('glogin'))

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = result.get('error')
        # response = make_response(json.dumps(result.get('error')), 500)
        # response.headers['Content-Type'] = 'application/json'
        flash(response)
        return redirect(url_for('glogin'))

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = "Token's user ID doesn't match given user ID."
        # response = make_response(json.dumps(response), 401)
        # response.headers['Content-Type'] = 'application/json'
        flash(response)
        return redirect(url_for('glogin'))

    # Verify that the access token is valid for this app.
    if result['issued_to'] != G_CLIENT_ID:
        response = "Token's client ID does not match app's."
        # response = make_response(json.dumps(response), 401)
        print response
        # response.headers['Content-Type'] = 'application/json'
        flash(response)
        return redirect(url_for('glogin'))

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = 'Current user is already connected.'
        # response = make_response(json.dumps(response), 200)
        # response.headers['Content-Type'] = 'application/json'
        flash(response)
        return redirect(url_for('showRestaurants'))

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(data['email'])
    if not user_id:
        newUser = createUser(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s in Google" % login_session['username'])
    print "done!"
    return redirect(url_for('showRestaurants'))

# #########################################################################
# DISCONNECT - Revoke a current user's token and reset their login_session
# #########################################################################

# ######################################
# Google Disconnect
# ######################################
# Route with Method: GET
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = 'Current user not connected.'
        # response = make_response(json.dumps(response), 401)
        # response.headers['Content-Type'] = 'application/json'
        flash(response)
        return redirect(url_for('glogin'))

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = 'Successfully disconnected from Google Plus.'
        # response = make_response(json.dumps(response), 200)
        # response.headers['Content-Type'] = 'application/json'
        flash(response)
    else:
        response = 'Failed to revoke token for given user.'
        # response = make_response(json.dumps(response, 400))
        # response.headers['Content-Type'] = 'application/json'
        flash(response)

    return redirect(url_for('glogin'))

# ######################################
# JSON APIs to view Restaurant Information
# ######################################

# ######################################
# Get Restaurant's in JSON Format
# ######################################
# Route with Method: GET
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


# ######################################
# Get Restaurant Menu's in JSON Format
# ######################################
# param (int) restaurant_id
# param (int) menu_id
# Route with Method: GET
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# ######################################
# Get Restaurant Menu Item in JSON Format
# ######################################
# param (int) restaurant_id
# param (int) menu_id
# Route with Method: GET
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


# ######################################
# Create a new restaurant
# ######################################
# Route with Method: GET and POST
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newRestaurant)
        flash('New Restaurant %s Successfully Created' % newRestaurant.name)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


# ######################################
# Edit a restaurant
# ######################################
# param (int) restaurant_id
# Route with Method: GET and POST
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()

    if 'username' not in login_session:
        return redirect('/login')
    if editedRestaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=editedRestaurant)


# ######################################
# Delete a restaurant
# ######################################
# param (int) restaurant_id
# Route with Method: GET
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()

    if 'username' not in login_session:
        return redirect('/login')
    if restaurantToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(restaurantToDelete)
        flash('%s Successfully Deleted' % restaurantToDelete.name)
        session.commit()
        return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)


# ######################################
# Show a restaurant menu
# ######################################
# param (int) restaurant_id
# Route with Method: GET
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)

    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    if 'username' not in login_session or creator is None:
        return render_template('publicmenu.html', items=items, restaurant=restaurant)
    else:
        return render_template('menu.html', items=items, restaurant=restaurant, creator=creator, login_session=login_session)


# ######################################
# Create a new menu item
# ######################################
# param (int) restaurant_id
# Route with Method: GET and POST
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'],
                           course=request.form['course'],
                           restaurant_id=restaurant_id,
                           user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# ######################################
# Edit a menu item
# ######################################
# param (int) restaurant_id
# param (int) menu_id
# Route with Method: GET and POST
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()

    if 'username' not in login_session:
        return redirect('/login')
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this menu item. Please create your own menu item in order to edit.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# ######################################
# Delete a menu item
# ######################################
# param (int) restaurant_id
# param (int) menu_id
# Route with Method: GET and POST
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()

    if 'username' not in login_session:
        return redirect('/login')
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)


# ######################################
# User Helper Functions
# ######################################

# ######################################
# Create User from login_session
# ######################################
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# ######################################
# Get User Info
# ######################################
# param (int) user_id
def getUserInfo(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except:
        return None


# ######################################
# Get User Id
# ######################################
# param (string) email
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# ######################################
# main function
# ######################################
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
