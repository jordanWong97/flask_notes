"""Flask app."""

from flask import Flask, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import CreateUserForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = "YOUR_SECRET"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

##############################################################################
#   USERS


@app.get('/')
def index():
    """Redirects to /register route"""

    return redirect('/register')


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """ Register user, if error, renders register page """

    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username,
                             password=password,
                             email=email,
                             first_name=first_name,
                             last_name=last_name)

        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.username

        flash(f"{username} account created")
        return redirect("/secret")

    else:
        return render_template(
            "register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """ Login user, if not valid user, redirect to login page """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.username
            return redirect("/secret")
        else:
            form.username.errors = ["Bad name/password"]


@app.get('/secret')
def show_secret():
    """Show hidden page for logged-in users only."""

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        return render_template("secret.html")
