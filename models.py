from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db =  SQLAlchemy()

def connect_db(app):
    """Wraps logic into a function connecting app to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Base class of common attributes shared by the tables inheriting User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable = False)
    type = db.Column(db.Text, nullable = False)
    rank = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    phone_number = db.Column(db.String)
    image_url = db.Column(
        db.Text,
        default="/static/images/REPLCO_logo.png",
    )
    bio = db.Column(db.Text)
    last_login = db.Column(db.DateTime)
    newSoldier_id = db.Column(db.Integer, db.ForeignKey('incoming.id', ondelete='cascade'))
    cadre_id = db.Column(db.Integer, db.ForeignKey('cadre.id', ondelete='cascade'))
    gainUnit_userid = db.Column(db.Integer, db.ForeignKey('gainers.id', ondelete='cascade'))

    # SQLAlchemy associations
    incoming = db.relationship('NewSoldier', backref=db.backref('incoming_user', uselist=False), foreign_keys=[newSoldier_id] )
    cadre = db.relationship('Cadre', backref=db.backref('cadre_user', uselist=False), foreign_keys=[cadre_id])
    gainers = db.relationship('GainingUser', backref=db.backref('gaining_user', uselist=False), foreign_keys=[gainUnit_userid])
    messages = db.relationship('Messages', backref='user')
    likes = db.relationship('Likes', backref='user')

    @classmethod
    def register(cls, username, pwd, email, type):
        """Register user with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal unicode utf8 string
        hashed_utf8 = hashed.decode("utf8")

        reg_user = cls(username=username, password=hashed_utf8, email=email, type=type)
        db.session.add(reg_user)
        return reg_user
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists and password is correct."""
        s = User.query.filter_by(username=username).first()
        if s and bcrypt.check_password_hash(s.password, pwd):
            return s
        else:
            return False

class NewSoldier(db.Model):
    """Models a new in-processing Soldier and inherits from User"""
    __tablename__ = 'incoming'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    arrival_datetime = db.Column(db.DateTime, nullable = False)
    report_bldg1020 = db.Column(db.Date)
    username = db.Column(db.Text, db.ForeignKey('users.username', ondelete='cascade'))

    # Initialed fields for accountability
    tele_recall = db.Column(db.Text)
    in_proc_hours = db.Column(db.Text)
    new_pt = db.Column(db.Text)
    uniform = db.Column(db.Text)
    transpo = db.Column(db.Text)

    orders = db.Column(db.Text)
    da31 = db.Column(db.Text)
    pov = db.Column(db.Text)
    flight = db.Column(db.Text)
    mypay = db.Column(db.Text)

    tdy = db.Column(db.Text)
    gtc = db.Column(db.Text)
    tla = db.Column(db.Text)
    hotels = db.Column(db.Text)
    
    def __repr__(self):
        """dunder method for easy representation of incoming Soldier object"""
        s = self
        return f"<New Soldier id={s.id} Rank={s.incoming_user.rank} FirstName={s.incoming_user.first_name} LastName={s.incoming_user.last_name} Arrival DateTime={s.arrival_datetime} Report Date={s.report_bldg1020} Phone number={s.incoming_user.phone_number} App username={s.username}>"  

    @property
    def rank_and_name(self):
        return self.incoming_user.rank + " " + self.incoming_user.last_name
    

class Cadre(db.Model):
    """Models a cadre user working at Replacement Company"""
    __tablename__ = 'cadre'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.Text)
    username = db.Column(db.Text, db.ForeignKey('users.username', ondelete='cascade'))

    @property
    def rank_and_name(self):
        return self.cadre_user.rank + " " + self.cadre_user.last_name

class GainingUser(db.Model):
    """Models a user from the gaining units"""
    __tablename__ = 'gainers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BDE = db.Column(db.Text)
    BN = db.Column(db.Text)
    unit = db.Column(db.Text)
    role = db.Column(db.Text)
    username = db.Column(db.Text, db.ForeignKey('users.username', ondelete='cascade'))

    @property
    def rank_and_name(self):
        return self.gaining_user.rank + " " + self.gaining_user.last_name

class Messages(db.Model):
    """Model for mini-blog message posts"""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    
class Likes(db.Model):
    """Model for liking message posts"""
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='cascade'))
