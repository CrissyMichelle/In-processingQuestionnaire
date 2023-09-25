from unittest import TestCase
from flask_wtf import FlaskForm
from forms import ArrivalForm
from app import app, db
from flask import get_flashed_messages
from models import User
from config import TestConfig
from seed import seed_database
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData, ForeignKeyConstraint
import logging
from werkzeug.datastructures import MultiDict
from datetime import datetime

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

csrf = CSRFProtect(app)

class IntegrationTestCases(TestCase):
    """Test the creation of a user and verify data gets pulled/updated in profile page"""
    def setUp(self):
        self.app = app
        app.config.from_object(TestConfig)
        sql_database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print('DEBUGGGGGGGGGGGINNNNNGGNGNGNGNGNGNGN', sql_database_uri)
        self.client = app.test_client()
        self.app_context = self.app.app_context()
        self.request_context = self.app.test_request_context()

        db.create_all()
        # seed_database()

        self.app.config['WTF_CSRF_ENABLED'] = False

        self.app_context.push()
        self.request_context.push()

    def tearDown(self):
        db.session.remove()

        db.engine.execute('DROP TABLE IF EXISTS incoming CASCADE;')
        db.engine.execute('DROP TABLE IF EXISTS cadre CASCADE;')
        db.engine.execute('DROP TABLE IF EXISTS gainers CASCADE;')
        db.engine.execute('DROP TABLE IF EXISTS users CASCADE;')

        db.session.rollback()
        
        self.request_context.pop()
        self.app_context.pop()

    def test_create_user_and_show_profile_page(self):
        with self.client:
            # Manually put test user into database
            user = User(username="test_user", password="securepassword", email="rex@email.com", type='incoming')
            db.session.add(user)
            db.session.commit

            # Manually mimic the session data of a logged-in user
            with self.client.session_transaction() as session:
                session['username'] = 'test_user'

            data = MultiDict({
                'datetime': datetime(2023, 8, 1, 6, 1),
                'rank':                    "PVT",            
                'f_name':                  "T" ,
                'l_name':                  "T" ,
                'report':                  datetime(2023, 8, 1, 6, 1)   , 
                'telephone':               "111-111-1111" ,
                'dodid':                   "1234567899", 
                'lose_UIC':                "WWW123" ,
                'gain_UIC':                "WWWaaa" ,
                'home_town':               "Podunk" ,
                'known_sponsor':           "TRUE"     ,
                'tele_recall':             "TT"     ,
                'in_proc_hours':           "TT"     ,
                'new_pt':                  "TT"     ,
                'uniform':                 "TT"     ,
                'transpo':                 "TT"     ,
                'orders':                  "TT" ,
                'da31':                    "TT" ,
                'pov':                     "TT"  ,   
                'flight':                  "TT"   ,  
                'mypay':                   "TT" ,
                'tdy':                     "TT"  ,   
                'gtc':                     "TT"   ,  
                'tla':                     "TT" ,
                'hotels':                  "TT" ,
                'read_acknowledgement':    "TRUE" 
            })
            form = ArrivalForm(formdata=data)
            self.assertTrue(form.validate())

            response = self.client.post('questionnaire', data=data, follow_redirects=True)

            self.assertIn(b'111-111-1111', response.data)

            self.assertEqual(response.status_code, 200)
            messages = get_flashed_messages()
            self.assertIn('Added Incoming User test_user', messages)
