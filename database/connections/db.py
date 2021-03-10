from flask_sqlalchemy import SQLAlchemy

# inititate SQLAlchemy object, which will link to our (Flask-)app 
# and look at all of the objects we tell it to and allow us to map all those objects to rows in the database; 
# e.g. it is goingto allow us to easily put an object (with certain rows and columns) into a database
#this is to tell our app that we have two models that are coming from tables in the database and how to read them
# -->(once "db.Model" is added to other model-classes)
db = SQLAlchemy()