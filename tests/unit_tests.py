from unittest import TestCase
from flask_wtf import FlaskForm
from forms import CreateUserForm
from app import app, db
from flask import get_flashed_messages
from models import User
from config import TestConfig
from seed import seed_database
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData, ForeignKeyConstraint
import logging
from werkzeug.datastructures import MultiDict

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

csrf = CSRFProtect(app)

class CreateUserFormTestCase(TestCase):
    """Uncover source of extra_validators error"""
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

    def test_username_field(self):
        with self.client:
            data = MultiDict({'username': "Rex", 'password': "securepassword", 'email': "rex@email.com"})
            form = CreateUserForm(formdata=data)
            print("HHHHEEEEEEEEEEEEEEEYYyYYyYYyyYYYYYYYYYYYYYYData before validation: ", form.data)
            if not form.validate():
                print("FORM FAILED VALIDATION!!!!!!!zxzxzxzxzxzxzxzxzxzxzxzx here are the errors: ", form.errors)
            self.assertTrue(form.validate())

    def test_unique_username(self):
        with self.client:
            with self.app.app_context():
                user1 = User(username="Rex", password="securepassword", email="rex@email.com", type='incoming')
                db.session.add(user1)
                db.session.commit()

            rex_from_db = User.query.filter_by(username='Rex').first()
            self.assertIsNotNone(rex_from_db)

            data2 = MultiDict({'username': "Rex", 'password': "securepassword", 'email': "rex@email.com"})
            form2 = CreateUserForm(formdata=data2)

            if form2.is_submitted() and not form2.validate():
                messages = get_flashed_messages()
                self.assertIn('Username already taken', messages)


    def test_password_length(self):
        with self.client:
            data = MultiDict({'username': "Rex", 'password': "short", 'email': "rex@email.com"})
            form = CreateUserForm(formdata=data)
            self.assertFalse(form.validate())
            print("Form errors: ", form.errors)
            self.assertIn('Must be at least 6 characters long.', form.password.errors)
        
    def test_email_field(self):
        with self.client:
            data = MultiDict({'username': "Rex", 'password': "securepassword", 'email': ""})
            form = CreateUserForm(formdata=data)
            print("Form errors: ", form.errors)
            self.assertFalse(form.validate())
            self.assertIn('This field is required.', form.email.errors)

