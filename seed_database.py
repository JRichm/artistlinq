from server import app
from model import db, connect_to_db, User
from datetime import datetime
import os

## do not create two databases on one system
## dev build uses art_station
os.system('dropdb -U postgres artistlinqdb')
os.system('createdb -U postgres artistlinqdb')

# Connect to the database
connect_to_db(app)

# Create the database tables
with app.app_context():
    db.create_all()

    # Create sample data
    user1 = User(
        username='user1',
        email='user1@example.com',
        password_hash='password1',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # Add data to the session and commit the changes
    with app.app_context():
        db.session.add(user1)
        db.session.commit()
        
