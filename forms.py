from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, StringField, SelectField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Regexp, DataRequired
from wtforms.widgets import Input

class HTML5DateField(StringField):
    """Render wtf DateField into a string for html purposes"""
    widget = Input(input_type='date')
class HTML5DateTimeField(StringField):
    """Render wtf DateTimeField into a string for html purposes"""
    widget = Input(input_type='datetime-local')


class ArrivalForm(FlaskForm):
    """Form for tracking incoming personnel."""
    # Arrival date and time
    datetime = HTML5DateTimeField('Arrival Date and Time', validators=[DataRequired()])
    
    # Rank and name
    rank = SelectField("rank", validators=[InputRequired()],
                       choices=[('PVT', 'PVT'), ('PV2', 'PV2'), ('PFC', 'PFC'), ('SPC', 'SPC'), ('CPL', 'CPL'),
                                ('SGT', 'SGT'), ('SSG', 'SSG'), ('SFC', 'SFC'),( 'MSG', 'MSG'), ('1SG', '1SG'),
                                ('SGM', 'SGM'), ('CSM', 'CSM'), ('SMA', 'SMA'),
                                ('2LT', '2LT'), ('1LT', '1LT'), ('CPT', 'CPT'), ('MAJ', 'MAJ'), ('LTC', 'LTC'),
                                ('COL', 'COL'), ('BG', 'BG'), ('MG', 'MG'), ('LTG', 'LTG'), ('GEN', 'GEN'), ('GA', 'GA'),
                                ('wo1', 'WO1'), ('CW2', 'CW2'), ('CW3', 'CW3'), ('CW4', 'CW4'), ('CW5', 'CW5')])
    f_name = StringField("first", validators=[InputRequired()])
    l_name = StringField("last", validators=[InputRequired()])

    # Report date
    report = HTML5DateField('Report to REPLCo on (YYYYMMDD)', validators=[DataRequired()])

    # Telephonic recall
    telephone = StringField('Telephone Number (XXX-XXX-XXXX)', validators=[
        DataRequired(),
        Regexp(r'^\d{3}-\d{3}-\d{4}$', message="Please enter a valid telephone number in the format XXX-XXX-XXXX.")
    ])

    # First blocks for initials
    tele_recall = StringField('2 HOUR TELEPHONIC RECALL (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    in_proc_hours = StringField('IN PROCESSING HOURS (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    new_pt = StringField("NEWCOMER'S PT (Initials)", validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    uniform = StringField('DUTY UNIFORM (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    transpo = StringField('TRANSPORTATION (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    # Finance initial blocks
    orders = StringField('PCS orders with amendments (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    da31 = StringField('DA Form 31 (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    pov = StringField('POV inspection/shipping form, marriage and birth certificates (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    flight = StringField('Flight Itinerary (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    mypay = StringField('MyPay Username and Password (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])

    # Final few initial blocks
    tdy = StringField('PERMISSIVE TEMPORARY DUTY (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    gtc = StringField('GOVERNMENT TRAVEL CARD (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    tla = StringField('TEMPORARY LODGING ALLOWANCE (TLA) (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    hotels = StringField('HOTELS/LODGING (Initials)', validators=[
        DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    
    read_acknowledgement = BooleanField("I have read and understand all information detailed above.", 
                                        validators=[DataRequired()])

    
class CreateUserForm(FlaskForm):
    """Form for adding new users"""
    username = StringField("user name", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging in existing users"""
    username = StringField("user name", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    