from flask import Flask, session, render_template, redirect, flash, session, url_for, request, jsonify, current_app
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from key import GOOGLE_MAPS_KEY
from models import db, connect_db, User, NewSoldier, Cadre, GainingUser, Messages
from forms import ArrivalForm, CreateUserForm, LoginForm, EnterEndpointForm, GetDirectionsForm, CustomFieldParam, GainersForm, CadreForm, MessageForm
import requests
import logging, datetime, traceback, sys, pdb
from datetime import datetime

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kbymaecc:hmiBfUsgWuKYu7elxc_Pt1-etdxWo-Md@bubble.db.elephantsql.com/kbymaecc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///inprocessing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = "psst420"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def to_register():
    """Redirects to page with registration form"""
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def signup_form():
    """Shows form for registering/creating a new user and handles submission."""
    # but first, logged in users can't create a new user
    if "username" in session:
        flash(f"You can create a new user. But {session['username']} must logout first!")
        return redirect(f"/users/{session['username']}")
    
    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        type = form.type.data
        
        new_user = User.register(username=username, pwd=password, email=email, type=type)
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

@app.route("/logout")
def logout():
    """Clears the browser session of username and redirects after grabbing logout time"""
    try:
        username = session['username']

        s = User.query.filter(User.username == username).one()
        s.last_login = datetime.utcnow()
        
        session.pop("username")
        return redirect("/login")
    except KeyError:
        return redirect("/register")

@app.route("/questionnaire", methods=["GET", "POST"])
def page_for_inproc_users():
    """Show and handle Replacement Company's incoming personnel questionaire"""
    # but first, make sure only logged in users can get here
    if "username" not in session:
        raise Unauthorized()

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
        
        # add newly-arrived Soldier data into database 
        new_arrived = NewSoldier(arrival_datetime = datetime, report_bldg1020 = report, username = incoming_user.username)
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
        raise Unauthorized()

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
        raise Unauthorized()

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
        raise Unauthorized()
    
    s = User.query.filter(User.username == username).one()
    soldier = s.incoming
    return render_template("users/deets.html", soldier=soldier)

@app.route("/users/gaining/<username>")
def show_gaining_user(username):
    """Info page for logged-in g-users"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    g = User.query.filter(User.username == username).one()
    gaining_unit_user = g.gainers
    return render_template("users/gainers.html", soldier=gaining_unit_user)

@app.route("/users/cadre/<username>")
def show_cadre_user(username):
    """Info page for logged-in cadre members"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    c = User.query.filter(User.username == username).one()
    cadre_user = c.cadre
    return render_template("users/cadre.html", soldier=cadre_user)

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
        #     return redirect("/directions?origin=Lyman Gate, HI&destination=" + end_point + "&mode=DRIVING")
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
    mode = request.args.get('mode', 'DRIVING')

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

@app.route('/users/show/<int:user_id>')
def show_user(user_id):
    """Shows user profile and user's messages"""

    user = User.query.get_or_404(user_id)

    messages = (Messages.query.filter(Messages.user_id == user_id)
                .order_by(Messages.timestamp.desc()).all())
    
    return render_template('users/show.html', user=user, messages=messages)
