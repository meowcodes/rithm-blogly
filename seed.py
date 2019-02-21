from models import User, db
from app import app

# Create all tables
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
whiskey = User(first_name='Whiskey', last_name="The Dog")
spike = User(first_name='Spike', last_name="The Porcupine")

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()