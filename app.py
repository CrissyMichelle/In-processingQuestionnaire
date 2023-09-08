from flask import Flask, session, render_template, redirect, flash, session, url_for, request, jsonify, current_app, abort
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
from werkzeug.exceptions import Unauthorized
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# from key import GOOGLE_MAPS_KEY, SECRET_KEY, SQLALCHEMY_DATABASE_URI, MAIL_PASSWORD, GET_EMAIL
from models import db, connect_db, User, NewSoldier, Cadre, GainingUser, Messages, Likes
from forms import ArrivalForm, CreateUserForm, LoginForm, EditUserForm, EnterEndpointForm, GetDirectionsForm, CustomFieldParam, GainersForm, CadreForm, MessageForm, AuthGetEmail
import logging, datetime, traceback, sys, pdb, requests, os
from datetime import datetime
import pandas as pd
from openpyxl import Workbook

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///inprocessing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.config['MAIL_SERVER'] = '127.0.0.1'
app.config['MAIL_PORT'] = '1025'
app.config['MAIL_USERNAME'] = 'crissymichelle@proton.me'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

with app.app_context():
    mail = Mail(app)
    connect_db(app)
    db.create_all()

@app.route("/")
def to_register():
    """Redirects to page with registration form"""
    if "username" in session:
        return redirect("/users/profile")
    else:
        return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def signup_form():
    """Shows form for registering/creating a new user and handles submission."""
    # but first, logged in users can't create a new user
    if "username" in session:
        flash(f"You can create a new user. But {session['username']} must logout first!")
        return redirect("/users/profile")
    
    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        type = form.type.data
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken, please choose another.")
            return render_template("register.html", form=form)
        
        new_user = User.register(username=username, pwd=password, email=email, type=type)
        db.session.add(new_user)
        db.session.commit()
        
        # put newly-created username into current browser session
        session['username'] = new_user.username
        flash(f"Added User {username}")

        if type == 'incoming':
            return redirect("/questionnaire")
        elif type == 'gainers':
            return redirect("/gainers_form")
        elif type == 'cadre':
            return redirect("/cadre_form")
    else:
        return render_template("register.html", form=form)
    
@app.route("/login", methods=["GET", "POST"])
def login_form():
    """Shows form for logging in users and handles form submission"""
    # but first, logged in users can't double tap login
    if "username" in session:
        flash(f"{session['username']} is already logged in!")
        return redirect(f"/users/{session['username']}")
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            app_user = User.query.filter(User.username == user.username).one()
            if app_user.type == 'incoming':
                return redirect(f"/users/{user.username}")
            elif app_user.type == 'gainers':
                return redirect(f"/users/gaining/{user.username}")
            elif app_user.type == 'cadre':
                return redirect(f"/users/cadre/{user.username}")
        else:
            form.username.errors = ["Bad username/password"]
            return render_template("login.html", form=form)
        
    return render_template("login.html", form=form)

@app.route("/send_email", methods=["GET", "POST"])
def send_email():
    """Send email to logged in cadre member"""

    if "username" not in session:
        # raise Unauthorized()
        return redirect("/register")
    
    username = session['username']
    cadre_user = User.query.filter(User.username == username).one()

    form = AuthGetEmail()
    entered_code = None
    correct_code = os.environ.get('GET_EMAIL')

    if form.validate_on_submit():
        entered_code = form.code.data
        
        if entered_code == correct_code:
            # Retrieve data from incoming users in the User class
            user_data = User.query.filter(and_(User.type == 'incoming', User.incoming.has(NewSoldier.arrival_datetime != None))).all()
            # Convert user data into a pandas data frame
            user_df = pd.DataFrame([(user.email, user.rank, user.first_name, user.last_name,
                                    user.phone_number, user.incoming.arrival_datetime,
                                    user.incoming.tele_recall,
                                    user.incoming.in_proc_hours,
                                    user.incoming.new_pt,
                                    user.incoming.uniform,
                                    user.incoming.transpo,
                                    user.incoming.orders,
                                    user.incoming.da31,
                                    user.incoming.pov,
                                    user.incoming.flight,
                                    user.incoming.mypay,
                                    user.incoming.tdy,
                                    user.incoming.gtc,
                                    user.incoming.tla,
                                    user.incoming.hotels) for user in user_data],
                                    columns=['Email', 'Rank', 'First', 'Last', 'Phone', 'Arrival Date',
                                            'Tele_recall', 'In_proc_Hours', 'Newcomer_PT', 'Duty_Uniform', 'Transpo',
                                            'PCS_orders', 'DA31', 'POV', 'Flight', 'MyPay', 'PTDY', 'GTC',
                                            'TLA', 'Hotels'])
            # Create excel file
            excel_path = 'user_data.xlsx'
            user_df.to_excel(excel_path, index=False)

            cadre_member = cadre_user.email

            msg = Message('Incoming REPLCo Personnel', sender='crissymichelle@proton.me', recipients=[cadre_member])
            msg.body = "See attached for incoming personnel data"
            with app.open_resource(excel_path) as fp:
                msg.attach(excel_path, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', fp.read())
            mail.send(msg)

            # Clean up by removing the excel file after sending
            os.remove(excel_path)

            flash('Email sent!')
            return redirect(f"users/cadre/{session['username']}")
        else:
            flash("Bad access code.")
            return redirect(f"users/cadre/{session['username']}")
    
    return render_template("send_email.html", form=form)

@app.route("/logout")
def logout():
    """Clears the browser session of username and redirects after grabbing logout time"""
    try:
        username = session['username']

        s = User.query.filter(User.username == username).one()
        s.last_login = datetime.utcnow()
        db.session.commit()
        
        session.pop("username")
        return redirect("/login")
    except KeyError:
        return redirect("/register")

@app.route("/questionnaire", methods=["GET", "POST"])
def page_for_inproc_users():
    """Show and handle Replacement Company's incoming personnel questionaire"""
    # but first, make sure only logged in users can get here
    if "username" not in session:
        # raise Unauthorized()
        return redirect("/register")

    form = ArrivalForm()

    if form.validate_on_submit():
        username = session['username']
        incoming_user = User.query.filter(User.username == username).one()

        # Airport arrival date
        datetime = form.datetime.data
        # Rank and name
        rank = form.rank.data
        f_name = form.f_name.data
        l_name = form.l_name.data
        # Report date
        report = form.report.data
        # Telephonic recall
        telephone = form.telephone.data
        # Initial blocks
        tele_recall     = form.tele_recall.data
        in_proc_hours   = form.in_proc_hours.data
        new_pt          = form.new_pt.data
        uniform         = form.uniform.data
        transpo         = form.transpo.data
        orders          = form.orders.data
        da31            = form.da31.data
        pov             = form.pov.data
        flight          = form.flight.data
        mypay           = form.mypay.data
        tdy             = form.tdy.data
        gtc             = form.gtc.data
        tla             = form.tla.data
        hotels          = form.hotels.data
        
        # add newly-arrived Soldier data into database 
        new_arrived = NewSoldier(arrival_datetime = datetime, report_bldg1020 = report, username = incoming_user.username,
                                tele_recall     = tele_recall,
                                in_proc_hours   = in_proc_hours,
                                new_pt          = new_pt,
                                uniform         = uniform,
                                transpo         = transpo,
                                orders          = orders,
                                da31            = da31,
                                pov             = pov,
                                flight          = flight,
                                mypay           = mypay,
                                tdy             = tdy,
                                gtc             = gtc,
                                tla             = tla,
                                hotels          = hotels)
        db.session.add(new_arrived)
        try:
            db.session.commit()
            # after linking with inherited newly-arrived, commit incoming_user
            incoming_user.newSoldier_id = new_arrived.id
            incoming_user.rank = rank
            incoming_user.first_name = f_name
            incoming_user.last_name = l_name
            incoming_user.phone_number = telephone

            db.session.commit()
        except IntegrityError:
            print("integrity Error: Possible duplicate entry or null value.")
            db.session.rollback()
        except SQLAlchemyError as e:
            print(f"GeneralSQLAlchemy Error: {e}")
            db.session.rollback()
        except Exception as e:
            print(f"Error while committing session: {e}")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            db.session.rollback()

        return redirect(f"/users/{session['username']}")
    
    print(form.errors)
    return render_template("questionnaire.html", form=form)

@app.route("/gainers_form", methods=["GET", "POST"])
def page_for_gaining_users():
    """Show and handle form for users receiving personnel"""
    # but first, make sure only logged in users can get here
    if "username" not in session:
        # raise Unauthorized()
        return redirect("/register")

    form = GainersForm()

    if form.validate_on_submit():
        username = session['username']
        gaining_user = User.query.filter(User.username == username).one()

        # Rank and name
        rank = form.rank.data
        f_name = form.f_name.data
        l_name = form.l_name.data
        # Unit data
        BDE = form.BDE.data
        BN = form.BN.data
        unit = form.unit.data
        # Role in gaining unit
        role = form.role.data
        # Telephonic recall
        telephone = form.telephone.data
        
        # add gaining-unit's Soldier data into database 
        gainer = GainingUser(BDE=BDE, BN=BN, unit=unit, role=role, username=gaining_user.username)
        db.session.add(gainer)
        try:
            db.session.commit()
            # after linking with inherited newly-arrived, commit incoming_user
            gaining_user.gainUnit_userid = gainer.id
            gaining_user.rank = rank
            gaining_user.first_name = f_name
            gaining_user.last_name = l_name
            gaining_user.phone_number = telephone

            db.session.commit()
        except IntegrityError:
            print("integrity Error: Possible duplicate entry or null value.")
            db.session.rollback()
        except SQLAlchemyError as e:
            print(f"GeneralSQLAlchemy Error: {e}")
            db.session.rollback()
        except Exception as e:
            print(f"Error while committing session: {e}")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            db.session.rollback()

        return redirect(f"users/gaining/{session['username']}")
    
    print(form.errors)
    return render_template("g-form.html", form=form)

@app.route("/cadre_form", methods=["GET", "POST"])
def page_for_cadre_users():
    """Show and handle form for Replacement Company cadre users"""
    # but first, make sure only logged in users can get here
    if "username" not in session:
        # raise Unauthorized()
        return redirect("/register")

    form = CadreForm()

    if form.validate_on_submit():
        username = session['username']
        cadre_user = User.query.filter(User.username == username).one()

        # Rank and name
        rank = form.rank.data
        f_name = form.f_name.data
        l_name = form.l_name.data

        # Role in Replacement Company organization
        role = form.role.data
        # Telephonic recall
        telephone = form.telephone.data
        
        # add gaining-unit's Soldier data into database 
        cadre = Cadre(role=role, username=cadre_user.username)
        db.session.add(cadre)
        try:
            db.session.commit()
            # after linking with inherited newly-arrived, commit incoming_user
            cadre_user.cadre_id = cadre.id
            cadre_user.rank = rank
            cadre_user.first_name = f_name
            cadre_user.last_name = l_name
            cadre_user.phone_number = telephone

            db.session.commit()
        except IntegrityError:
            print("integrity Error: Possible duplicate entry or null value.")
            db.session.rollback()
        except SQLAlchemyError as e:
            print(f"GeneralSQLAlchemy Error: {e}")
            db.session.rollback()
        except Exception as e:
            print(f"Error while committing session: {e}")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            db.session.rollback()

        return redirect(f"users/cadre/{session['username']}")
    
    print(form.errors)
    return render_template("c-form.html", form=form)

@app.route("/users/<username>")
def show_user_deets(username):
    """Info page for logged-in-users"""
    if "username" not in session or username != session['username']:
        # raise Unauthorized()
        return redirect("/register")
    
    try:
        s = User.query.filter(User.username == username).one()
        soldier = s.incoming
        return render_template("users/deets.html", soldier=soldier)
    except:
        return redirect("/questionnaire")

@app.route("/users/gaining/<username>")
def show_gaining_user(username):
    """Info page for logged-in g-users"""
    if "username" not in session or username != session['username']:
        # raise Unauthorized()
        return redirect("/register")
    
    try:
        g = User.query.filter(User.username == username).one()
        gaining_unit_user = g.gainers
        return render_template("users/gainers.html", soldier=gaining_unit_user)
    except:
        return redirect("/gainers_form")

@app.route("/users/cadre/<username>")
def show_cadre_user(username):
    """Info page for logged-in cadre members"""
    if "username" not in session or username != session['username']:
        # raise Unauthorized()
        return redirect("/register")
    
    try:
        c = User.query.filter(User.username == username).one()
        cadre_user = c.cadre
        form = AuthGetEmail()

        return render_template("users/cadre.html", soldier=cadre_user, form=form)
    except:
        return redirect("/cadre_form")

@app.route("/users/profile")
def show_profile_page():
    """Redirect to user's profile details"""
    if "username" in session:
        username = session['username']

        try:
            u = User.query.filter(User.username == username).one()
            if u.type == "incoming":
                return redirect(f"/users/{username}")
            elif u.type == "gainers":
                return redirect(f"/users/gaining/{username}")
            else:
                return redirect(f"/users/cadre/{username}")
        except:
            return redirect("/register")
        
    else:
        return redirect("/register")

@app.route("/users/edit/<username>", methods=["GET", "POST"])
def edit_profile(username):
    """Update profile for current user"""
    if "username" not in session or username != session['username']:
        return redirect("/register")
    u = User.query.filter(User.username == username).one()

    form = EditUserForm()
    if form.validate_on_submit():
        editing_user = User.authenticate(u.username, form.password.data)
        if editing_user:
            try:
                editing_user = User.query.get(u.id)

                if form.email.data:    
                    editing_user.email=form.email.data
                if form.rank.data:    
                    editing_user.rank=form.rank.data
                if form.f_name.data:    
                    editing_user.first_name=form.f_name.data
                if form.l_name.data:    
                    editing_user.last_name=form.l_name.data
                if form.telephone.data:    
                    editing_user.phone_number=form.telephone.data
                if form.image_url.data:
                    editing_user.image_url=form.image_url.data
                if form.bio.data:
                    editing_user.bio=form.bio.data

                db.session.commit()
                return redirect("/users/profile")
                
            except IntegrityError: 
                flash("Issue with form validation", 'danger')                      
                return render_template("users/edit.html", form=form)            
        flash("Bad Password", 'danger')
        return redirect("/")
    
    else:
        return render_template("users/edit.html", form=form, soldier=u)

@app.route('/get_all_users')
def list_users():
    """Pass every user from db to front end"""
    all_users = User.query.all()

    all_incoming = NewSoldier.query.all()
    incoming_names = [{"name": incoming.rank_and_name, "id": incoming.incoming_user.id} for incoming in all_incoming]

    all_gainers = GainingUser.query.all()
    gainer_names = [{"name": gainer.rank_and_name, "id": gainer.gaining_user.id} for gainer in all_gainers]
    
    all_cadre = Cadre.query.all()
    cadre_names = [{"name": cadre.rank_and_name, "id": cadre.cadre_user.id} for cadre in all_cadre]

    return jsonify(incoming_names=incoming_names, gainer_names=gainer_names, cadre_names=cadre_names)

    
@app.route('/users/show/<int:user_id>')
def show_user(user_id):
    """Shows user profile and user's messages"""

    user = User.query.get_or_404(user_id)

    messages = (Messages.query.filter(Messages.user_id == user_id)
                .order_by(Messages.timestamp.desc()).all())
    # for message in messages:
    #     message.num_likes = Likes.query.filter_by(message_id=message.id).count()

    # likes = [like.message for like in user.likes]
    # for like in likes:
    #     like.num_likes = Likes.query.filter_by(message_id=like.id).count()
    
    return render_template('users/show.html', user=user, messages=messages)

@app.route("/users/<username>/delete", methods=["GET", "POST"])
def show_delete_page(username):
    """Show page for deletion based on logged in username in session"""
    if "username" not in session or username != session['username']:
         raise Unauthorized()

    s = User.query.filter(User.username == username).one()
    soldier = s.incoming
    # if POST request, we'll go ahead and delete the user
    if request.method == 'POST':
        db.session.delete(s)
        db.session.commit()
        session.pop("username")
    # and redirect to the login page
        return redirect("/login")

    return render_template("/users/delete.html", soldier=soldier)

@app.route("/resources", methods=["GET", "POST"])
def show_useful_links():
    """Show page with links and API functionality"""

    form = EnterEndpointForm()
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if form.validate_on_submit():
            end_point = form.destination.data
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Form not validated")
    
    return render_template("links.html", form=form)


@app.route("/api/directions")
def get_directions_for_api_call():
    """Use API to get directions"""

    start = request.args.get('origin')
    end = request.args.get('destination')
    mode = request.args.get('mode')

    data = {
        "origin":  start,
        "destination":  end,
        "travelMode":  mode}

    return jsonify(data)

@app.route("/directions", methods=["GET", "POST"])
def show_get_directions():
    """Render HTML page showing google map and form for api call.  Accepts parameters as query strings"""

    start = request.args.get('origin', 'Lyman Gate, HI')
    end = request.args.get('destination', '')
    mode = request.args.get('mode', 'WALKING')

    form = GetDirectionsForm()
    return render_template("directions.html", origin=start, destination=end, mode=mode, form=form)

@app.route('/messages/new', methods=["GET", "POST"])
def messages_add():
    """Add a message:
    Show form if GET. If valid, update message and redirect to show messages page.
    """

    if "username" not in session:
        flash("You must be logged in to see messages!", "danger")
        return redirect("/")
    username = session['username']

    form = MessageForm()

    if form.validate_on_submit():
        if username:
            app_user = User.query.filter(User.username == username).one()
        msg = Messages(text=form.text.data, timestamp=datetime.utcnow())
        app_user.messages.append(msg)
        db.session.commit()

        return redirect(f"/messages/show")

    return render_template('messages/new.html', form=form)

@app.route('/messages/show')
def show_messages():
    """Render page showing all messages"""

    if "username" not in session:
        flash("You must be logged in to see messages!", "danger")
        return redirect("/")
    username = session['username']
    app_user = User.query.filter(User.username == username).one()

    messages = Messages.query.all()
    return render_template('messages/show.html', messages=messages, user=app_user)



# @app.route('/messages/<int:message_id>/like', methods=["POST"])
# def add_like(message_id):
#     """Adds a message to a user's likes"""

#     if "username" not in session:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")
    
#     username = session['username']
#     app_user = User.query.filter(User.username == username).first()
        
    
#     liked_message = Messages.query.get_or_404(message_id)
#     # a user cannot like their own messages
#     if liked_message.user_id == app_user.id:
#         return abort(403)
    
#     existing_like = Likes.query.filter(
#         Likes.message_id == liked_message.id,
#         Likes.user_id == app_user.id
#     ).first()

#     if existing_like is None:
#         new_like = Likes(user_id=app_user.id, message_id=liked_message.id)
#         db.session.add(new_like)
#         db.session.commit()
#         return jsonify({'status': 'success', 'message': "Message liked!", 'action': 'increment'}), 200
#     else:
#         db.session.delete(existing_like)
#         db.session.commit()
#         return jsonify({'status': 'failure', 'message': "Message unliked.", 'action': 'decrement'}), 200

    
