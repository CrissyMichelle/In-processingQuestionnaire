from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db =  SQLAlchemy()

def connect_db(app):
    """Wraps logic into a function connecting app to database"""
    db.app = app
    db.init_app(app)

class NewSoldier(db.Model):
    """Models a new in-processing Soldier"""
    __tablename__ = 'incoming'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    arrival_datetime = db.Column(db.DateTime, nullable = False)
    rank = db.Column(db.Text, nullable = False)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    report_bldg1020 = db.Column(db.Date)
    phone_number = db.Column(db.String)
    username = db.Column(db.String(20), db.ForeignKey('soldiers.username'))
    
    def __repr__(self):
        """dunder method for easy representation of incoming Soldier object"""
        s = self
        return f"<New Soldier id={s.id} Rank={s.rank} FirstName={s.first_name} LastName={s.last_name} Arrival DateTime={s.arrival_datetime} Report Date={s.report_bldg1020} Phone number={s.phone_number} App username={s.username}>"  

    @property
    def rank_and_name(self):
        return self.rank + " " + self.last_name
    
    app_user = db.relationship("Soldier", backref="new_Soldier",
                               cascade="all,delete")


class Soldier(db.Model):
    """Equivalent to a 'User' model"""
    __tablename__ = 'soldiers'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable = False)


    @classmethod
    def register(cls, username, pwd, email):
        """Register user with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal unicode utf8 string
        hashed_utf8 = hashed.decode("utf8")

        reg_user = cls(username=username, password=hashed_utf8, email=email)
        db.session.add(reg_user)
        return reg_user
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists and password is correct."""
        s = Soldier.query.filter_by(username=username).first()
        if s and bcrypt.check_password_hash(s.password, pwd):
            return s
        else:
            return False

    