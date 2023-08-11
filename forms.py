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

class CustomFieldParam(StringField):
    def __init__(self, *args, sub_label=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.sub_label = sub_label


class ArrivalForm(FlaskForm):
    """Form for tracking incoming personnel."""
    # Arrival date and time
    datetime = HTML5DateTimeField('1.Arrival Date and Time:', validators=[DataRequired()])
    
    # Rank and name
    rank = SelectField("Rank:", validators=[InputRequired()],
                       choices=[('PVT', 'PVT'), ('PV2', 'PV2'), ('PFC', 'PFC'), ('SPC', 'SPC'), ('CPL', 'CPL'),
                                ('SGT', 'SGT'), ('SSG', 'SSG'), ('SFC', 'SFC'),( 'MSG', 'MSG'), ('1SG', '1SG'),
                                ('SGM', 'SGM'), ('CSM', 'CSM'), ('SMA', 'SMA'),
                                ('2LT', '2LT'), ('1LT', '1LT'), ('CPT', 'CPT'), ('MAJ', 'MAJ'), ('LTC', 'LTC'),
                                ('COL', 'COL'), ('BG', 'BG'), ('MG', 'MG'), ('LTG', 'LTG'), ('GEN', 'GEN'), ('GA', 'GA'),
                                ('wo1', 'WO1'), ('CW2', 'CW2'), ('CW3', 'CW3'), ('CW4', 'CW4'), ('CW5', 'CW5')])
    f_name = StringField("First Name:", validators=[InputRequired()])
    l_name = StringField("Last Name:", validators=[InputRequired()])

    # Report date
    report = HTML5DateField('Report at 0845 hrs on [select a date] to Building 1020, Schofield Barracks, Hawaii 96857', validators=[DataRequired()])

    # Telephonic recall
    telephone = StringField('2.Contact Phone Number (XXX-XXX-XXXX):',
                            validators=[DataRequired(), Regexp(r'^\d{3}-\d{3}-\d{4}$',message="Please enter a valid telephone number in the format XXX-XXX-XXXX.")])

    # First blocks for initials
    tele_recall = CustomFieldParam('2 HOUR TELEPHONIC RECALL', sub_label='While Assigned to U.S. Army Hawaii Reception Company, you may be contacted telephonically.  This ensures all Cadre members are able to contact you for accountability and in case any emergency situation may arise. (Initials)',
                              validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    in_proc_hours = CustomFieldParam('3.IN PROCESSING HOURS', sub_label='Your place of duty throughout the week is detailed in the attached weekly schedule that you have received.  All Soldiers will attend all briefs and mandatory events.  Appointments will not be made that conflict with the installation in-processing timeline, Monday through Thursday. (Initials)',
                                validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    new_pt = CustomFieldParam("4.NEWCOMER'S PT:", sub_label="All Soldiers will report to Weyand Field at 0545 hours for Accountability/PT formation on Tuesday.  Uniform is SummerAPFU, running shoes with white or black socks covering the ankles, and a water source. (Initials)",
                         validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    uniform = CustomFieldParam('5.DUTY UNIFORM:',  sub_label='Authorized Combat Uniforms, Patrol Cap, and combat boots are the only authorized duty uniform while you are in-processing.  Your uniform and accessories will be IAW AR 670-1. (Initials)',
                          validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    transpo = CustomFieldParam('6.TRANSPORTATION:', sub_label='There is a daily courtesy shuttle pick up for all in-processing personnel who require transportation.  If you need transportation, contact U.S. Army Hawaii Reception Company CQ at 808-655-0389 or the Transportation Desk at 808-859-5784 the day prior to schedule for pick-up. (Initials)',
                          validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
   
    # Finance initial blocks
    orders = StringField('a.PCS orders with amendments (Initials)',
                         validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    da31 = CustomFieldParam('b.DA Form 31', sub_label='Leave Form with blocks #14 and #16 signed. (Initials)',
                       validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    pov = StringField('c.POV inspection/shipping form, marriage and birth certificates (Initials)',
                      validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    flight = StringField('d.Flight Itinerary (Initials)', validators=[DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    mypay = StringField('e.MyPay Username and Password (Initials)', validators=[DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])

    # Final few initial blocks
    tdy = CustomFieldParam("8.PERMISSIVE TEMPORARY DUTY:", sub_label="U.S. Army Hawaii Reception Company is not authorized to put you on PTDY.  All PTDY questions will be brought up to the Housing Services Office at 808-275-3700.  Approving authority for PTDY is your gaining unit's responsibility. (Initials)",
                      validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    gtc = CustomFieldParam('9.GOVERNMENT TRAVEL CARD:', sub_label='When you come to formation on the first day of in-processing please have your Government Travel Card balance ready.  This balance will be needed when you fill out your 1351-2 (Travel Voucher) for your PCS on the first day of in-processing.  The Citibank phone number to obtain your balance is 1-800-200-7056.  Please have this balance available and ensure that you check the split disbursement box on your Travel Voucher using the balance given by the Citibank representative. (Initials)',
                      validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    tla = CustomFieldParam('10.TEMPORARY LODGING ALLOWANCE (TLA):', sub_label='In order to receive TLA entitlements, ALL in-processing Soldiers (regardless of rank) are required to sign-in off of leave and receive a brief during the in-processing schedule that explains the steps you must take to reeive these entitlements. (Initials)',
                      validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
    ])
    hotels = CustomFieldParam('11.HOTELS/LODGING:', sub_label='Please ensure that you are staying at a TLA approved hotel in order to receive TLA entitlements. (Initials)',
                         validators=[DataRequired(),Regexp(r'^[A-Z]{2,4}$', message="Please enter 2 to 3 uppercase letters as initials.")
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

class EnterEndpointForm(FlaskForm):
    """Form for selecting endpoint"""
    end_point = StringField("End Point: ", validators=[InputRequired()])
    