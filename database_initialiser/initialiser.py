""" Functionality to Extend Flask Script ss"""
from sqlalchemy import exc
from flask_script import Command
from app import db, encrypt
from app.api.user.models import User
from app.api.widget.models import Widget, Fizzler, Banger

database = [
    {
        "model": User,
        "data": [
            {"FirstName": "Mike", "LastName": 'Jordan', "UserName": 'MJ', "Email": "mj@mysite.com"},
            {"FirstName": "Jnr", "LastName": 'Jordan', "UserName": 'JJ', "Email": "jj@mysite.com"}
        ]
    },
    {
        "model": Widget,
        "data": [
            {"Name": "WX5", "Size": "2XL"}
        ]
    },
    {
        "model": Fizzler,
        "data": [
            {"Name": "FZ_900", "Color": "Red", "Speed": 20.0, "WidgetID": 1}
        ]
    },
    {
        "model": Banger,
        "data": [
            {"Type": "YLW", "WidgetID": 1},
            {"Type": "BLK", "WidgetID": 1},
        ]
    }
]

class Initialiser(Command):
    """ Initialise Test Database
    """
    def run(self):
        """
        """
        if (input(
                "Are you sure you want to drop all tables and recreate? (y/N)\n").\
            lower() == "y"):
            
            print("Dropping tables...")
            db.drop_all()
            db.create_all()
            for table in database:
                if table["model"] == User:
                    pass
                    #TODO hash password when inserting. 
                else:
                    try:
                        db.session.bulk_insert_mappings(table["model"], table["data"])
                        db.session.commit()
                        print(f"{table['model'].__tablename__} initialised.")
                    except exc.SQLAlchemyError:
                        print(f"{table['model'].__tablename__} failed.")
            
            print("Database created.")