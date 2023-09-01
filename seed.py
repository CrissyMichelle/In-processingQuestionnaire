"""Seed file to make sample data for inprocessing database"""
from models import User, NewSoldier, Cadre, GainingUser, Messages, Likes, db
from sqlalchemy import text
from app import app
from datetime import datetime

# Create all tables after a total wipe

with app.app_context():
    db.engine.execute("DROP TABLE IF EXISTS users CASCADE")
with app.app_context():
    db.engine.execute("DROP TABLE IF EXISTS cadre CASCADE")
with app.app_context():
    db.engine.execute("DROP TABLE IF EXISTS incoming CASCADE")
with app.app_context():
    db.engine.execute("DROP TABLE IF EXISTS gainers CASCADE")

db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
NewSoldier.query.delete()
Cadre.query.delete()
GainingUser.query.delete()
Messages.query.delete()
Likes.query.delete()

# Create base User objects
snuffle = User(username='snuffle23', password ='passWORD!!123', email="joe.q.snuffy.mil@army.mil", type="incoming",
               rank='PVT', first_name="Joe",
                    last_name="Snuffy", phone_number='555-666-7474')

wardawg = User(username='wardawg', password ='killKillKILL', email="claude.v.dayum.mil@army.mil", type="incoming",
               rank='SSG', first_name="Claude",
                    last_name="Dayum")

captain = User(username='cptO3', password ='cpt03', email="jack.b.reacher.mil@army.mil", type="cadre",
               rank='CPT', first_name="Jack",
                    last_name="Reacher", phone_number='808-555-6464')

april = User(username='aprilmay93', password ='sfc23', email="april.o.neal.mil@army.mil", type="gainers",
               rank='SSG', first_name="April",
                    last_name="ONeal", phone_number='610-999-0990')

# Add and commit the base User objects
db.session.add(snuffle)
db.session.add(wardawg)
db.session.add(captain)
db.session.add(april)
db.session.commit()

# Create sample personnel objects linked to pre-committed base User objects
snuffy = NewSoldier(id=10986474, arrival_datetime=datetime(2023, 8, 1, 6, 1), username=snuffle.username)
warrior = NewSoldier(id=28034500, arrival_datetime=datetime(2023, 8, 4, 4), username=wardawg.username)
reacher = Cadre(id=64888999, role='commander', username=captain.username)
oneal = GainingUser(id=9999999, BDE='3IBCT', BN='3-4CAV', role="squad leader", username=april.username)
# Link the inheriting objects with the base class.  SQLA takes care of all the details!
snuffle.newSoldier_id = snuffy.id
wardawg.newSoldier_id = warrior.id
captain.cadre_id = reacher.id
april.gainUnit_userid = oneal.id
# Add and commit NewSoldier, Cadre, and GainingUser objects
db.session.add(snuffy)
db.session.add(warrior)
db.session.add(reacher)
db.session.add(oneal)
db.session.commit()

message1 = Messages(text="seeding database", timestamp = datetime(2023, 8, 22, 8, 22), user_id = wardawg.id)
db.session.add(message1)
db.session.commit()

like1 = Likes(user_id = snuffle.id, message_id = message1.id)
db.session.add(like1)
db.session.commit()