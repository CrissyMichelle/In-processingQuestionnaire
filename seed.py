"""Seed file to make sample data for inprocessing database"""
from models import User, NewSoldier, Cadre, GainingUser, Messages, db
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

# Create base User objects
snuffle = User(username='snuffle23', password ='passWORD!!123', email="joe.q.snuffy.not@4real.com", type="incoming",
               rank='PVT', first_name="Joe", last_name="Snuffy", phone_number='555-666-7474')

wardawg = User(username='wardawg', password ='killKillKILL', email="claude.v.dayum.not@4real.com", type="incoming",
               rank='SSG', first_name="Claude", last_name="Dayum")

captain = User(username='cptO3', password ='cpt03', email="jack.b.reacher.not@4real.com", type="cadre",
               rank='CPT', first_name="Jack", last_name="Reacher", phone_number='808-555-5555')
me = User(username='cmc', password ='123456', email="xxxxxx.x.xxxxxxx@notmail.com", type="cadre",
               rank='SFC', first_name="Michelle", last_name="Cobra", phone_number='777-777-7777',
               image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQAL8dUDsl1jHCZ-BMdHXLm4FOexiZnf6KBSA&usqp=CAU',
               bio='From a nice hometown, been in the Army 16 years, lifelong learner. I love using emerging tech to help out my fellow Soldiers!')

april = User(username='aprilmay93', password ='sfc23', email="april.o.neal.not@4real.com", type="gainers",
               rank='SSG', first_name="April", last_name="ONeal", phone_number='610-999-0990')
yody = User(username='yodyyolo', password ='654321', email="yannick.q.yaetz49.not@4real.com", type="gainers",
               rank='SGT', first_name="Yan", last_name="Yaetz", phone_number='111-999-0990')

# Add and commit the base User objects
db.session.add(snuffle)
db.session.add(wardawg)
db.session.add(captain)
db.session.add(me)
db.session.add(april)
db.session.add(yody)
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
reacher = Cadre(id=64888999, role='Automation OIC', username=captain.username)
author = Cadre(id=888888888, role='Software Dev', username=me.username)
oneal = GainingUser(id=9999999, BDE='3IBCT', BN='3-4CAV', role="squad leader", username=april.username)
yolo = GainingUser(id=8899999, BDE='2IBCT', BN='1-27', unit="A Co.", role="squad leader", username=yody.username)
# Link the inheriting objects with the base class.  SQLA takes care of all the details!
snuffle.newSoldier_id = snuffy.id
wardawg.newSoldier_id = warrior.id
captain.cadre_id = reacher.id
me.cadre_id = author.id
april.gainUnit_userid = oneal.id
yody.gainUnit_userid = yolo.id
# Add and commit NewSoldier, Cadre, and GainingUser objects
db.session.add(snuffy)
db.session.add(warrior)
db.session.add(reacher)
db.session.add(author)
db.session.add(oneal)
db.session.add(yolo)
db.session.commit()

message1 = Messages(text="where can i get vegan poke?", timestamp = datetime(2023, 9, 22, 8, 22), user_id = wardawg.id)
db.session.add(message1)
db.session.commit()
message2 = Messages(text="chess is the best", timestamp = datetime(2023, 8, 23, 16, 21), user_id = me.id)
db.session.add(message2)
message3 = Messages(text="you is the best", timestamp = datetime(2023, 8, 23, 16, 22), user_id = april.id)
db.session.add(message3)
message4 = Messages(text="YODY!!", timestamp = datetime(2023, 9, 7, 15, 21), user_id = yody.id)
db.session.add(message4)
db.session.commit()