from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from urlparse import parse_qs, urlparse

#from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base = declarative_base()
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

            debug = False
            message = ""

            if self.path.endswith("/restaurants/new"):

                output = ""
                output += "<html><body>"
                output += "<h1>Add Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/Insert'>'''
                output += '''<input name="restaurant_id" type="hidden" value="" >'''
                output += '''Name: <input name="restaurant_name" type="text" value="" >'''
                output += '''<br><br>'''
                output += '''<input type="submit" value="Add">'''
                output += '''</form>'''
                output += "<p>&nbsp;</p>"
                output += "</body></html>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(output)
                print output
                return

            elif self.path.startswith("/restaurants/Edit"):

                restaurant_id = 0

                url = self.path
                parse_string = parse_qs(url)
                page_info = urlparse(url)

                for qs in page_info.query.split("&"):
                    item = qs.split("=")
                    if item[0] == "id":
                        restaurant_id = item[1]

                output = ""
                output += "<html><body>"
                output += "<h1>Update Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/Update'>'''
                output += '''<input name="restaurant_id" type="hidden" value="%s" >'''
                output += '''Name: <input name="restaurant_name" type="text" value="%s" >'''
                output += '''<br><br>'''
                output += '''<input type="submit" value="Update">'''
                output += '''</form>'''
                output += "<p>&nbsp;</p>"
                output += "</body></html>"

                restaurant = get_row_restaurant(restaurant_id, "")

                # reset id
                restaurant_id = 0

                if restaurant.count() != 0:
                    restaurant_id = restaurant[0].id
                    restaurant_name = restaurant[0].name

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = (output) % (restaurant_id, restaurant_name)

                self.wfile.write(output)
                print output
                return

            elif self.path.startswith("/restaurants/Delete"):

                delete = False
                restaurant_id = 0

                url = self.path
                parse_string = parse_qs(url)
                page_info = urlparse(url)

                for qs in page_info.query.split("&"):
                    item = qs.split("=")
                    if item[0] == "id":
                        restaurant_id = item[1]

                output = ""
                output += "<html><body>"
                output += "<h1>Delete Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/Remove'>'''
                output += '''<input name="restaurant_id" type="hidden" value="%s" >'''
                output += '''Are you sure, you want to delete the restaurant?'''
                output += '''<br><br>'''
                output += '''<input type="submit" value="Yes">'''
                output += '''<input type="button" value="No" onclick="window.location=\'/restaurants\';">'''
                output += '''</form>'''
                output += "<p>&nbsp;</p>"
                output += "</body></html>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = (output) % (restaurant_id)

                self.wfile.write(output)
                print output
                return

            else:
                # display home page
                pageHome(self, "")
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:

            debug = False
            message = ""

            # Parse the form data posted
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })

            if debug == True:
                # Begin the response
                self.send_response(200)
                self.end_headers()
                self.wfile.write('Client: %s\n' % str(self.client_address))
                self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
                self.wfile.write('Path: %s\n' % self.path)
                self.wfile.write('Form data:\n')

                # Echo back information about what was posted in the form
                for field in form.keys():
                    field_item = form[field]
                    if field_item.filename:
                        # The field contains an uploaded file
                        file_data = field_item.file.read()
                        file_len = len(file_data)
                        del file_data
                        self.wfile.write('\tUploaded %s as "%s" (%d bytes)\n' % \
                                (field, field_item.filename, file_len))
                    else:
                        # Regular form value
                        self.wfile.write('\t%s=%s\n' % (field, form[field].value))

                self.wfile.write('\n')


            if self.path.startswith("/restaurants/Insert"):

                insert = False
                message = "The restaurant is added"

                restaurant_name = form['restaurant_name'].value

                if debug == True:
                    self.wfile.write('\tAction = Insert\n')
                    self.wfile.write('\tRestaurant Name: %s\n' % (restaurant_name))

                restaurant = get_row_restaurant("", restaurant_name)

                if restaurant.count() == 0:
                    insert = set_row_restaurant('INSERT', "", restaurant_name)

                if insert != True:
                    message = "Unable to add the restaurant name"

                if debug == True:
                    self.wfile.write('\tInsert: %s\n' % (insert))
                    return

            elif self.path.startswith("/restaurants/Update"):

                update = False
                message = "The restaurant is updated"

                restaurant_id = form['restaurant_id'].value
                restaurant_name = form['restaurant_name'].value

                if debug == True:
                    self.wfile.write('\tAction = Update\n')
                    self.wfile.write('\tRestaurant ID: %s\n' % (restaurant_id))
                    self.wfile.write('\tRestaurant Name: %s\n' % (restaurant_name))

                restaurant = get_row_restaurant(restaurant_id, "")

                if restaurant.count() != 0:
                    update = set_row_restaurant('UPDATE', restaurant[0].id, restaurant_name)

                if update != True:
                    message = "Unable to update the restaurant name"

                if debug == True:
                    self.wfile.write('\tUpdate: %s\n' % (update))
                    return

            elif self.path.startswith("/restaurants/Remove"):

                remove = False
                message = "The restaurant is deleted"

                restaurant_id = form['restaurant_id'].value

                if debug == True:
                    self.wfile.write('\tAction = Remove\n')
                    self.wfile.write('\tRestaurant ID: %s\n' % (restaurant_id))

                restaurant = get_row_restaurant(restaurant_id, "")

                if restaurant.count() != 0:
                    remove = delete_row_restaurant(restaurant_id)

                if remove != True:
                    message = "Unable to delete the restaurant name"

                if debug == True:
                    self.wfile.write('\tRemove: %s\n' % (remove))
                    return

            else:

                message = "Unable to complete your request"

                if debug == True:
                    self.wfile.write('<p>Unable to complete your request</p>')
                    return

            # display home page
            pageHome(self, message)
            return

        except IOError:
            self_obj.send_error(404, 'File Not Found: %s' % self_obj.path)


def get_list_restaurants():

    try:
        restaurants = session.query(Restaurant.id, Restaurant.name)

        if restaurants.count() != 0:
            result = ""
            for row in restaurants:
                result += "<p>"
                result += ("%s <br>") % (row.name)
                result += ("<a href=\'/restaurants/Edit?id=%s\'>Edit</a>&nbsp;&nbsp;"
                    "<a href=\'/restaurants/Delete?id=%s\'>Delete</a>") % (row.id, row.id)
                result += "</p>"
        else:
            result = "<p>No restaurants</p>"

    except:
        raise

    return result


def get_row_restaurant(restaurant_id, restaurant_name):

    result = ""
    try:
        if restaurant_id == "":
            restaurant = session.query(Restaurant.id, Restaurant.name).\
                filter(Restaurant.name==restaurant_name)
        else:
            restaurant = session.query(Restaurant.id, Restaurant.name).\
                filter(Restaurant.id==restaurant_id)

        result = restaurant

    except:
        raise

    return result


def set_row_restaurant(action, restaurant_id, restaurant_name):

   result = False
   try:
       if action == 'UPDATE':
           session.query(Restaurant.id).\
                filter(Restaurant.id == restaurant_id).\
                update({'name': restaurant_name})
           session.commit()
           result = True
       else:
           myRestaurant = Restaurant(name=restaurant_name)
           session.add(myRestaurant)
           session.commit()

           result = True


   except:
       session.rollback()
       result = False

   return result


def delete_row_restaurant(restaurant_id):

   result = False
   try:
       session.query(Restaurant.id).\
            filter(Restaurant.id == restaurant_id).\
            delete()
       session.commit()
       result = True


   except:
       session.rollback()
       result = False

   return result


def pageHome(self_obj, message):
    try:
        self_obj.send_response(200)
        self_obj.send_header('Content-type', 'text/html')
        self_obj.end_headers()

        restaurants = get_list_restaurants()

        output = ""
        output += "<html><body>"

        if message != "":
            output += ("<h2 style='color:red;'>%s</h2>" % (message))

        output += "<h1>Restaurants List</h1>"
        output += "<p><a href=\'/restaurants/new\'>Add a Restaurant</a></p>"
        output += "%s"
        output += "<p>&nbsp;</p>"
        output += "</body></html>"

        self_obj.wfile.write((output) % (restaurants))
        print output

    except IOError:
        self_obj.send_error(404, 'File Not Found: %s' % self_obj.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
