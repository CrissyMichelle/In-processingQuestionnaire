from flask import Flask, session, render_template, redirect, flash, session, url_for, request
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import db, connect_db, NewSoldier, Soldier
from forms import ArrivalForm, CreateUserForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kbymaecc:hmiBfUsgWuKYu7elxc_Pt1-etdxWo-Md@bubble.db.elephantsql.com/kbymaecc'
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

        new_user = Soldier.register(username=username, pwd=password, email=email)
        db.session.commit()
        
        # put newly-created username into current browser session
        session['username'] = new_user.username
        flash(f"Added Soldier {username}")

        return redirect("/secret")
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

        user = Soldier.authenticate(username, password)

        if user:
            session['username'] = user.username 
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad username/password"]
            return render_template("login.html", form=form)
        
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Clears the browser session of username and redirects"""
    session.pop("username")
    return redirect("/")

@app.route("/secret", methods=["GET", "POST"])
def page_for_reg_users():
    """Show and handle Replacement Company's incoming personnel questionaire"""
    # but first, make sure only logged in users can get here
    if "username" not in session:
        raise Unauthorized()

    form = ArrivalForm()

    if form.validate_on_submit():
        print("Form validated")
        datetime = form.datetime.data

    
        # Rank and name
        rank = form.rank.data
        f_name = form.f_name.data
        l_name = form.l_name.data

        # Report date
        report = form.report.data

        # Telephonic recall
        telephone = form.telephone.data
        
        # put newly-arrived Soldier data into database
        new_arrived = NewSoldier(arrival_datetime = datetime,
                                 rank = rank, first_name = f_name,
                                 last_name = l_name, report_bldg1020 = report,
                                 phone_number = telephone,
                                 username = session['username'])
        db.session.add(new_arrived)
        try:
            db.session.commit()
            print(f"NewEmp created with username {session['username']}")
        except Exception as e:
            print(f"Error while committing session: {e}")
            db.session.rollback()

        return redirect(f"/users/{session['username']}")
    
    print("Form not validated or not a POST request")
    print(form.errors)
    return render_template("secret.html", form=form)

@app.route("/users/<username>")
def show_user_deets(username):
    """Info page for logged-in-users"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    s = Soldier.query.get(username)
    soldier = s.new_Soldier[0]
    return render_template("users/deets.html", soldier=soldier)

@app.route("/users/<username>/delete", methods=["GET", "POST"])
def show_delete_page(username):
    """Show page for deletion based on logged in username in session"""
    if "username" not in session or username != session['username']:
         raise Unauthorized()
     
    s = Soldier.query.get(username)
    soldier = s.new_Soldier[0]
    # if POST request, we'll go ahead and delete the user
    if request.method == 'POST':
        db.session.delete(s)
        db.session.commit()
        session.pop("username")
    # and redirect to the login page
        return redirect("/login")

    return render_template("/users/delete.html", soldier=soldier)
