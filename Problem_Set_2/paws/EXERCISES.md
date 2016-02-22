Exercise 1 - Setting up views

Take a moment to plan out the user experience for your website. Use all of the skills you learned in lessons 3 and 4 to iteratively create a functioning Flask web application that works with your database of puppies. Think of all of the navigation use cases for your site. Create page mockups and then design a web application that facilitates this process.

In your Python code, you should add methods for performing all of the database functionalities described below:
All CRUD operations on Puppies, Shelters, and Owners
Switching or Balancing Shelter Population and Protecting against overflows
Viewing a Puppy Profile
Adopting a New Puppy
Creating and Styling Templates (optionally with Bootstrap)
Adding Flash Messages
BONUS: Pagination

----------------------------------------------------

Exercise 2 - Application Structure for a large Flask Project

Up until now, most of our Python code for creating Flask projects has lived in two files. We’ve been calling them database_setup.py and project.py. Using a minimal number of python files is great for learning how Flask works but as an application grows and becomes more complex, reorganizing this code into different files makes navigating code easier and identifying concerns in a more modular fashion more doable. For this exercise you will rearrange your code into a package making your code more manageable.
Where do I start?

Read through Flask documentation on packages: http://flask.pocoo.org/docs/0.10/patterns/packages/

Explore Flask also has some good literature on packages: https://exploreflask.com/organizing.html#organization-patterns

Create a package for your application complete with an init.py file, views.py, models.py, and any other smaller modules you see fit to better organize your application. Discuss your package organization with other students.

----------------------------------------------------

Exercise 3 - Using Flask Extensions

Flask is designed to be a very lightweight and minimalist framework upon installation, giving the programmer much more control over design decisions when creating a web application. Flask extensions are packages created by other developers to allow additional functionalities to be added quickly and easily.

In this activity you should learn about flask extensions and specifically read about WTForms. What features does WTForms provide compared to collecting form data manually? Add the WTForms package to your application and implement its code when you collect form data and add some validation rules that prevent poorly formatted information from being saved to the database (blank first or last name, email address without “@” or “.”)
Where do I start?

Flask documentation on extensions: http://flask.pocoo.org/docs/0.10/extensiondev/ A registry of available Flask extensions: http://flask.pocoo.org/extensions/ Documenation for WTForms: http://wtforms.readthedocs.org/en/latest/ Form Validation with WTForms: http://flask.pocoo.org/docs/0.10/patterns/wtforms/

----------------------------------------------------

Exercise 4 - Logging

Logging is a great way of tracking app use and behavior for when the unexpected occurs. Logging also helps create a paper trail in case any abnormal activity or behavior happens on your app.

For this exercise, you will go to the Flask documentation again and figure out how to log information to a text file any time a puppy is added or adopted.
Where do I start?

Flask documentation on logging: http://flask.pocoo.org/docs/0.10/quickstart/#logging
Feeling Extra Udacious?

Good logging ensures good communication between the developers and those responsible for maintaining an app once it’s up and running. (IT or DevOps). Delve deeper into good logging practices and consider implementing some of the following features into your application.

log rotation: If you server process keeps appending to the same log file forever, eventually it will fill up the disk ... it should probably close the file and start a new one periodically

remote logging / log saving : how do you get my logs off of the individual container and into permanent storage?

log merging: Let's say your application has 10 servers; a user query could go to any of them; how could you merge the logs so that you can find all transactions?

query logging vs. exception / debug logging: logging different issues into different files

----------------------------------------------------

Exercise 5 - Email/SMS Support

Being able to provide feedback via email is a part of almost every web application experience nowadays. Integrating email support in Flask has been simplified with the Flask-Mail extension. For this exercise send an email or SMS to the owner each time a puppy is adopted.
Where do I start?

Check out this page about the Flask-Mail extension: https://pythonhosted.org/flask-mail/

Twilio has an SMS python package that can be easily used with Flask, check out this tutorial: https://www.twilio.com/blog/2012/01/making-an-sms-birthday-card-with-python-and-flask.html

    Spam Alert!

    If your application lets people enter unconfirmed email addresses, your app may be vulnerable to being compromised by a spambot. Account confirmation via email is a good way to circumvent this problem. In later exercises you will have challenges to confirm user accounts via email.

----------------------------------------------------

Exercise 6 - User Authentication

If you’ve already taken the course on Authentication and Authorization, you know that implementing secure user authentication on a web application can be a very difficult task to complete.

Using OAuth providers can simplify the user authentication process for you and your users. But in some cases it may be necessary to implement user authentication on your own.

For this challenge, you will add user authentication using either an OAuth provider, implementing your own user logins or if you’re feeling extra ambitious, a hybridized approach that allows both login options. You can consider the potential owners as the users of the application.

This challenge will be tough. You may want to wait until you’ve completed Authentication and Authorization before attempting this challenge. As always, please reach out for help if you get stuck and be sure to give yourself a pat on the back once you’ve completed this exercise.

If you do chose to implement your own user authentication please be sure all of the following features are implemented in your application:

Using the right Authentication
Extensions for Flask
Hashing Passwords with Werkzeug
Creating an Authentication Blueprint
New User Registration
Account Confirmation
Password reset/recovery

Where do I start?

Udacity's course on Authentication and Authorization http://udacity.com/course/ud330 Documentation for the Flask-Security Extension https://pythonhosted.org/Flask-Security/
Feeling Extra Udacious?

Add profile pages for each user and create roles for an anonymous user, a logged in user, and an administrator with different view options and permissions.

----------------------------------------------------

Exercise 7 - Testing & Performance

Up to this point, you’ve created a pretty complex application. So how can you be sure everything is working correctly? Testing your application is a way to find bugs before your users do. In addition, even if there are no coding bugs, maybe some performance issues might create a less than pleasant user experience for visitors to your page. In this exercise you will read about Coverage, The Flask Test Client, and Selenium in order to create a test suite for your application. You should also find a way to identify and log slow queries to address performance issues that arise with a growing database. Share your testing strategy with other students and view the strategies they implemented as well.
Where Do I Start?

Check out this article about testing in Flask: https://flask-testing.readthedocs.org/en/latest/

Flask Documentation of Testing: http://flask.pocoo.org/docs/0.10/testing/

Documentation on Coverage: http://nedbatchelder.com/code/coverage/

----------------------------------------------------

Exercise 8 - Deployment

Ready to take your application live? It’s time to deploy your application and share it with other Udacians and the whole world. Deploying can be a challenge the first time around but keep at it and use all of your resources to get your app properly functioning on the web.
Where Do I Start?

Check out this article on Deployment from Explore Flask: https://exploreflask.com/deployment.html

----------------------------------------------------


Going Further
Here are a few more features you could add to your website, the possibilities are endless so feel free to challenge yourself and and more improvements to your puppy adoption website!
Full Text Search Feature

Adding full text search can be a complicated task. If you are up for the challenge take a look at this blog post by Miguel Grinberg and see if you can add search functionality to your web application:

http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-full-text-search

Add a searchable feature to your database, search for a dog by name and return the results of that search with relevant information in the search results. Make a query in SQLAlchemy that returns all of the shelters that have a dog named 'Rudy', sort results by shelter name, and by puppy age.
AJAX

AJAX (Asynchronous JavaScript and XML) is a popular way of delivering data to a webpage without prompting a page refresh. When used appropriately, integrating AJAX into a web application can have a great impact on the user experience. For this exercise, you will return search results using AJAX instead of rendering a new web page.
Where do I start?

http://flask.pocoo.org/docs/0.10/patterns/jquery/
