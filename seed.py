"""Seed file to make sample data for inprocessing database"""
from models import NewSoldier, Soldier, db
from app import app
from datetime import datetime

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
NewSoldier.query.delete()
Soldier.query.delete()

# Create sample personnel objects
snuffy = NewSoldier(arrival_datetime=datetime(2023, 8, 1, 6, 1), rank='PVT', first_name="Joe",
                    last_name="Snuffy", phone_number='555-666-7474', username="snuffle23")
snuffle = Soldier(username='snuffle23', password ='passWORD!!123', email="joe.q.snuffy.mil@army.mil")

warrior = NewSoldier(arrival_datetime=datetime(2023, 8, 4, 4), rank='SSG', first_name="Claude",
                    last_name="Dayum", username="wardawg")
wardawg = Soldier(username='wardawg', password ='killKillKILL', email="claude.v.dayum.mil@army.mil")

# Add and commit new objects
db.session.add(snuffy)
db.session.add(snuffle)
db.session.add(warrior)
db.session.add(wardawg)

db.session.commit()