from os import environ
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from app import create_app

app = create_app(environ.get("FLASK_ENV", 'development'))
db = SQLAlchemy(app)

# Import models after db initialised but before Migration
from app.api.user.models import *

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()


@manager.command
def init_db():
    print('Creating database...')
    db.create_all()


@manager.command
@manager.command
def drop_all():
    if input("Are you sure you want to drop all tables? (y/N)\n").lower() == "y":
        print("Dropping tables...")
        db.drop_all()



if __name__ == "__main__":
    manager.run()