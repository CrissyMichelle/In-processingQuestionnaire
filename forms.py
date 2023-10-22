from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, StringField, SelectField, PasswordField, BooleanField, ValidationError, TextAreaField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Regexp, DataRequired, Length, Email
from wtforms.widgets import Input

# @overwrite:
# def validate(self, extra_validators=None):
#     initial_validation = super(FlaskForm, self).validate(extra_validators)


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


class ValidGeoLocation:
    """Validates input sent to Google Maps API"""
    def __init__(self, message=None):
        if not message:
            message = 'Please enter a valid address or LatLng.  (For example "Wahiawa, HI" or 21.497,-158.068).'
        self.message = message

    def __call__(self, form, field):
        pass


class ArrivalForm(FlaskForm):
    """Form for tracking incoming personnel."""

    # custom validator for dodid field
    def validate_dodid_length(form, field):
        if len(str(field.data)) != 10:
            raise ValidationError('Please enter your DODID as numbers only.')
    # Arrival date and time
    datetime = HTML5DateTimeField('1.Arrival Date and Time:', validators=[DataRequired()])
    
    # Rank and name
    rank = SelectField("Rank:", validators=[InputRequired()],
                       choices=[('PVT', 'PVT'), ('PV2', 'PV2'), ('PFC', 'PFC'), ('SPC', 'SPC'), ('CPL', 'CPL'),
                                ('SGT', 'SGT'), ('SSG', 'SSG'), ('SFC', 'SFC'), ('MSG', 'MSG'), ('1SG', '1SG'),
                                ('SGM', 'SGM'), ('CSM', 'CSM'), ('SMA', 'SMA'),
                                ('2LT', '2LT'), ('1LT', '1LT'), ('CPT', 'CPT'), ('MAJ', 'MAJ'), ('LTC', 'LTC'),
                                ('COL', 'COL'), ('BG', 'BG'), ('MG', 'MG'), ('LTG', 'LTG'), ('GEN', 'GEN'), ('GA', 'GA'),
                                ('wo1', 'WO1'), ('CW2', 'CW2'), ('CW3', 'CW3'), ('CW4', 'CW4'), ('CW5', 'CW5')])
    f_name = StringField("First Name:", validators=[InputRequired()])
    l_name = StringField("Last Name:", validators=[InputRequired()])

    # Report date
    report = HTML5DateField('Report at 0845 hrs on date below (auto-populated) to Building 1020, Menoher Rd, Schofield Barracks, Hawaii 96857.',
                            validators=[DataRequired()])

    # Telephonic recall
    telephone = StringField('2.Contact Phone Number (XXX-XXX-XXXX):',
                            validators=[DataRequired(), Regexp(r'^\d{3}-\d{3}-\d{4}$', message="Please enter a valid telephone number in the format XXX-XXX-XXXX.")])

    # Late addition fields
    dodid = IntegerField("DODID:", validators=[DataRequired(), validate_dodid_length])
    lose_UIC = StringField("Losing Unit UIC:", validators=[DataRequired(), Length(min=6, message='UIC must be at least 6 characters long.')])
    gain_UIC = StringField("Gaining Unit UIC:", validators=[DataRequired(), Length(min=6, message='UIC must be at least 6 characters long.')])
    home_town = StringField("Home of Record:", validators=[DataRequired()])
    known_sponsor = SelectField("You know your sponsor...True or False?", validators=[DataRequired()], choices=[('TRUE', 'TRUE'), ('FALSE', 'FALSE')])

    # First blocks for initials
    tele_recall = CustomFieldParam('2 HOUR TELEPHONIC RECALL', sub_label='While Assigned to U.S. Army Hawaii Reception Company, you may be contacted telephonically.  This ensures all Cadre members are able to contact you for accountability and in case any emergency situation may arise. (Initials)',
                              validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    in_proc_hours = CustomFieldParam('3.IN PROCESSING HOURS', sub_label='Your place of duty throughout the week is detailed in the attached weekly schedule that you have received.  All Soldiers will attend all briefs and mandatory events.  Appointments will not be made that conflict with the installation in-processing timeline, Monday through Thursday. (Initials)',
                                validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    new_pt = CustomFieldParam("4.NEWCOMER'S PT:", sub_label="All Soldiers will report to Weyand Field at 0545 hours for Accountability/PT formation on Tuesday.  Uniform is SummerAPFU, running shoes with white or black socks covering the ankles, and a water source. (Initials)",
                         validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    uniform = CustomFieldParam('5.DUTY UNIFORM:',  sub_label='Authorized Combat Uniforms, Patrol Cap, and combat boots are the only authorized duty uniform while you are in-processing.  Your uniform and accessories will be IAW AR 670-1. (Initials)',
                          validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    transpo = CustomFieldParam('6.TRANSPORTATION:', sub_label='There is a daily courtesy shuttle pick up for all in-processing personnel who require transportation.  If you need transportation, contact U.S. Army Hawaii Reception Company CQ at 808-655-0389 or the Transportation Desk at 808-859-5784 the day prior to schedule for pick-up. (Initials)',
                          validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
   
    # Finance initial blocks
    orders = StringField('a.PCS orders with amendments (Initials)',
                         validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    da31 = CustomFieldParam('b.DA Form 31', sub_label='Leave Form with blocks #14 and #16 signed. (Initials)',
                       validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    pov = StringField('c.POV inspection/shipping form, marriage and birth certificates (Initials)',
                      validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    flight = StringField('d.Flight Itinerary (Initials)', validators=[DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    mypay = StringField('e.MyPay Username and Password (Initials)', validators=[DataRequired(),
        Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])

    # Final few initial blocks
    tdy = CustomFieldParam("8.PERMISSIVE TEMPORARY DUTY (PTDY):", sub_label="U.S. Army Hawaii Reception Company is not authorized to put you on PTDY.  All PTDY questions will be brought up to the Housing Services Office at 808-275-3700.  Approving authority for PTDY is your gaining unit's responsibility. (Initials)",
                      validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    gtc = CustomFieldParam('9.GOVERNMENT TRAVEL CARD (GTC):', sub_label='When you come to formation on the first day of in-processing please have your Government Travel Card balance ready.  This balance will be needed when you fill out your 1351-2 (Travel Voucher) for your PCS on the first day of in-processing.  The Citibank phone number to obtain your balance is 1-800-200-7056.  Please have this balance available and ensure that you check the split disbursement box on your Travel Voucher using the balance given by the Citibank representative. (Initials)',
                      validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    tla = CustomFieldParam('10.TEMPORARY LODGING ALLOWANCE (TLA):', sub_label='In order to receive TLA entitlements, ALL in-processing Soldiers (regardless of rank) are required to sign-in off of leave and receive a brief during the in-processing schedule that explains the steps you must take to reeive these entitlements. (Initials)',
                      validators=[DataRequired(), Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    hotels = CustomFieldParam('11.HOTELS/LODGING:', sub_label='Please ensure that you are staying at a TLA approved hotel in order to receive TLA entitlements. (Initials)',
                         validators=[DataRequired(),Regexp(r'^[A-Z]{2,4}$', message="Please enter your initials as 2 uppercase letters.")
    ])
    
    read_acknowledgement = BooleanField("I have read and understand all information detailed above.", 
                                        validators=[DataRequired()])

    
class CreateUserForm(FlaskForm):
    """Form for adding new users"""
    # overide the behind-the-scenes validate() function call by explicitly setting the extra_validators arg to None.
    # def validate(self):
    #     initial_validation = super(CreateUserForm, self).validate(extra_validators=None)

    #     if not self.username.data or not self.username.data.strip():
    #         self.username.errors.append('This field is required.')
    #         return False
        
    #     return initial_validation and True
    code = PasswordField("Verification code")
    username = StringField("user name", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired(), Length(min=6, message='Must be at least 6 characters long.')])
    email = StringField("email", validators=[InputRequired()])


class GainersForm(FlaskForm):
    """Form for adding new gaining-unit users"""
    rank = SelectField("Rank:", validators=[InputRequired()],
                       choices=[('PVT', 'PVT'), ('PV2', 'PV2'), ('PFC', 'PFC'), ('SPC', 'SPC'), ('CPL', 'CPL'),
                                ('SGT', 'SGT'), ('SSG', 'SSG'), ('SFC', 'SFC'), ('MSG', 'MSG'), ('1SG', '1SG'),
                                ('SGM', 'SGM'), ('CSM', 'CSM'), ('SMA', 'SMA'),
                                ('2LT', '2LT'), ('1LT', '1LT'), ('CPT', 'CPT'), ('MAJ', 'MAJ'), ('LTC', 'LTC'),
                                ('COL', 'COL'), ('BG', 'BG'), ('MG', 'MG'), ('LTG', 'LTG'), ('GEN', 'GEN'), ('GA', 'GA'),
                                ('wo1', 'WO1'), ('CW2', 'CW2'), ('CW3', 'CW3'), ('CW4', 'CW4'), ('CW5', 'CW5')])
    f_name = StringField("First Name:", validators=[InputRequired()])
    l_name = StringField("Last Name:", validators=[InputRequired()])
    BDE = StringField("Brigade:", validators=[InputRequired()])
    BN = StringField("Battalion:", validators=[InputRequired()])
    unit = StringField("Unit:", validators=[InputRequired()])
    role = StringField("Role or Position:", validators=[InputRequired()])
    telephone = StringField('Contact Phone Number (XXX-XXX-XXXX):',
                            validators=[DataRequired(), Regexp(r'^\d{3}-\d{3}-\d{4}$',message="Please enter a valid telephone number in the format XXX-XXX-XXXX.")])


class CadreForm(FlaskForm):
    """Form for adding cadre users"""
    rank = SelectField("Rank:", validators=[InputRequired()],
                       choices=[('PVT', 'PVT'), ('PV2', 'PV2'), ('PFC', 'PFC'), ('SPC', 'SPC'), ('CPL', 'CPL'),
                                ('SGT', 'SGT'), ('SSG', 'SSG'), ('SFC', 'SFC'), ('MSG', 'MSG'), ('1SG', '1SG'),
                                ('SGM', 'SGM'), ('CSM', 'CSM'), ('SMA', 'SMA'),
                                ('2LT', '2LT'), ('1LT', '1LT'), ('CPT', 'CPT'), ('MAJ', 'MAJ'), ('LTC', 'LTC'),
                                ('COL', 'COL'), ('BG', 'BG'), ('MG', 'MG'), ('LTG', 'LTG'), ('GEN', 'GEN'), ('GA', 'GA'),
                                ('wo1', 'WO1'), ('CW2', 'CW2'), ('CW3', 'CW3'), ('CW4', 'CW4'), ('CW5', 'CW5')])
    f_name = StringField("First Name:", validators=[InputRequired()])
    l_name = StringField("Last Name:", validators=[InputRequired()])

    role = StringField("Role or Position:", validators=[InputRequired()])
    telephone = StringField('Contact Phone Number (XXX-XXX-XXXX):',
                            validators=[DataRequired(), Regexp(r'^\d{3}-\d{3}-\d{4}$',message="Please enter a valid telephone number in the format XXX-XXX-XXXX.")])


class LoginForm(FlaskForm):
    """Form for logging in existing users"""
    username = StringField("user name", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])


class EnterEndpointForm(FlaskForm):
    """Form for selecting endpoint"""
    destination = StringField("Destination: ", validators=[InputRequired()])


class GetDirectionsForm(FlaskForm):
    """Form for Google Maps API"""
    origin = StringField("Origin: ", validators=[InputRequired(), ValidGeoLocation()])
    destination = StringField("Destination: ", validators=[InputRequired(), ValidGeoLocation()])
    travelMode = SelectField("Select an option:", validators=[InputRequired()],
                             choices=[("DRIVING", "Driving"), ("WALKING", "Walking"), ("BICYCLING", "Biking"),
                                      ("TRANSIT", "Public Transit")])
    

class MessageForm(FlaskForm):
    """Form for adding/editing messages"""
    text = TextAreaField('text', validators=[DataRequired()])


class AARcommentsForm(FlaskForm):
    """Form for giving feedback to Reception Co."""
    text = TextAreaField('text', validators=[DataRequired()])


class EditUserForm(FlaskForm):
    """Form for editing user profiles"""
    
    email = StringField('email')
    alt_email = StringField('Alternative or civilian email')
    rank = SelectField("Rank:", validators=[InputRequired()],
                       choices=[('No Change', 'rank --No Change--'), ('PVT', 'PVT'), ('PV2', 'PV2'), ('PFC', 'PFC'), ('SPC', 'SPC'), ('CPL', 'CPL'),
                                ('SGT', 'SGT'), ('SSG', 'SSG'), ('SFC', 'SFC'), ('MSG', 'MSG'), ('1SG', '1SG'),
                                ('SGM', 'SGM'), ('CSM', 'CSM'), ('SMA', 'SMA'),
                                ('2LT', '2LT'), ('1LT', '1LT'), ('CPT', 'CPT'), ('MAJ', 'MAJ'), ('LTC', 'LTC'),
                                ('COL', 'COL'), ('BG', 'BG'), ('MG', 'MG'), ('LTG', 'LTG'), ('GEN', 'GEN'), ('GA', 'GA'),
                                ('wo1', 'WO1'), ('CW2', 'CW2'), ('CW3', 'CW3'), ('CW4', 'CW4'), ('CW5', 'CW5')])
    f_name = StringField('First Name')
    l_name = StringField('Last Name')
    role = StringField('Role or Position')
    telephone = StringField('Phone Number')
    image_url = StringField('Profile Pic url')
    bio = StringField('Bio')
    
    password = PasswordField('Password', validators=[Length(min=6)])


class AuthGetEmail(FlaskForm):
    """Form authorizing email with spreadsheet"""

    code = PasswordField("Enter access code", validators=[DataRequired()])
    submit = SubmitField("Email spreadsheet")


class AuthGetAARs(FlaskForm):
    """Form authorizing email with spreadsheet"""

    code = PasswordField("Enter access code", validators=[DataRequired()])
    submit = SubmitField("Email AARs")
