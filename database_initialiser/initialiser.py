from sqlalchemy import exc
from flask_script import Command
from app import db
from app.api.user.models import User

database = [
    {
        "model": User,
        "data": [
            {"FirstName": "Mike", "LastName": 'Jordan', "UserName": 'MJ', "Email": "mj@mysite.com"},
            {"FirstName": "Jnr", "LastName": 'Jordan', "UserName": 'JJ', "Email": "jj@mysite.com"}
        ]
    }
]

class Initialiser(Command):
    def run(self):
        if (
            input(
                "Are you sure you want to drop all tables and recreate? (y/N)\n"
            ).lower()
            == "y"):
            
            print("Dropping tables...")
            db.drop_all()
            db.create_all()
            for table in database:
                try:
                    db.session.bulk_insert_mappings(table["model"], table["data"])
                    db.session.commit()
                    print(f"{table['model'].__tablename__} initialised.")
                except exc.SQLAlchemyError:
                    print(f"{table['model'].__tablename__} failed.")
            
            print("Database created.")