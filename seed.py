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
               rank='PVT', first_name="Joe", last_name="Snuffy", phone_number='555-666-7474')

wardawg = User(username='wardawg', password ='killKillKILL', email="claude.v.dayum.mil@army.mil", type="incoming",
               rank='SSG', first_name="Claude", last_name="Dayum")

captain = User(username='cptO3', password ='cpt03', email="jack.b.reacher.mil@army.mil", type="cadre",
               rank='CPT', first_name="Jack", last_name="Reacher", phone_number='808-555-6464')
me = User(username='cmc', password ='123456', email="crissy.m.cabrera.mil@army.mil", type="cadre",
               rank='MSG', first_name="Crissy", last_name="Cabrera", phone_number='757-575-7479',
               image_url='https://wwd.com/wp-content/uploads/2016/11/usk-10228r2.jpg?w=800')

april = User(username='aprilmay93', password ='sfc23', email="april.o.neal.mil@army.mil", type="gainers",
               rank='SSG', first_name="April", last_name="ONeal", phone_number='610-999-0990')

# Add and commit the base User objects
db.session.add(snuffle)
db.session.add(wardawg)
db.session.add(captain)
db.session.add(me)
db.session.add(april)
db.session.commit()

# Create sample personnel objects linked to pre-committed base User objects
snuffy = NewSoldier(id=10986474, arrival_datetime=datetime(2023, 8, 1, 6, 1), username=snuffle.username,
    tele_recall = 'JS',
    in_proc_hours = 'JS',
    new_pt = 'JS',
    uniform = 'JS',
    transpo = 'JS',
    orders = 'JS',
    da31 = 'JS',
    pov = 'JS',
    flight = 'JS',
    mypay = 'JS',
    tdy = 'JS',
    gtc = 'JS',
    tla = 'JS',
    hotels = 'JS')
warrior = NewSoldier(id=28034500, arrival_datetime=datetime(2023, 8, 4, 4), username=wardawg.username,
    tele_recall = 'CD',
    in_proc_hours = 'CD',
    new_pt = 'CD',
    uniform = 'CD',
    transpo = 'CD',
    orders = 'CD',
    da31 = 'CD',
    pov = 'CD',
    flight = 'CD',
    mypay = 'CD',
    tdy = 'CD',
    gtc = 'CD',
    tla = 'CD',
    hotels = 'CD')
reacher = Cadre(id=64888999, role='commander', username=captain.username)
author = Cadre(id=888888888, role='Software Dev', username=me.username)
oneal = GainingUser(id=9999999, BDE='3IBCT', BN='3-4CAV', role="squad leader", username=april.username)
# Link the inheriting objects with the base class.  SQLA takes care of all the details!
snuffle.newSoldier_id = snuffy.id
wardawg.newSoldier_id = warrior.id
captain.cadre_id = reacher.id
me.cadre_id = author.id
april.gainUnit_userid = oneal.id
# Add and commit NewSoldier, Cadre, and GainingUser objects
db.session.add(snuffy)
db.session.add(warrior)
db.session.add(reacher)
db.session.add(author)
db.session.add(oneal)
db.session.commit()

message1 = Messages(text="seeding database", timestamp = datetime(2023, 8, 22, 8, 22), user_id = wardawg.id)
db.session.add(message1)
db.session.commit()
message2 = Messages(text="chess is the best", timestamp = datetime(2023, 8, 23, 16, 21), user_id = me.id)
db.session.add(message2)
message3 = Messages(text="you is the best", timestamp = datetime(2023, 7, 23, 16, 21), user_id = april.id)
db.session.add(message3)
db.session.commit()

like1 = Likes(user_id = snuffle.id, message_id = message1.id)
like2 = Likes(user_id = snuffle.id, message_id = message2.id)

db.session.add(like1)
db.session.add(like2)
db.session.commit()