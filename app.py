"""Flask app."""

from flask import Flask, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Note
from forms import CreateUserForm, LoginForm, CSRFProtectForm, CreateNoteForm


app = Flask(__name__)

app.config['SECRET_KEY'] = "YOUR_SECRET"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connect_db(app)
# db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

##############################################################################
#   USERS


@app.get('/')
def index():
    """Redirects to /register route"""
# TODO:check if session and go to users page

    return redirect('/register')


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """ Register user, if error, renders register page """
    # breakpoint()
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
    # TODO: check for dupe names, query the table to see if  the username or email exist

        db.session.add(user)
        db.session.commit()
        # change to username
        session['username'] = user.username

        flash(f"{username} account created")
        return redirect(f"/users/{user.username}")

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
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
    else:
        form.username.errors = ["Bad name/password"]
        return render_template('login.html', form=form)


@app.get('/users/<username>')
def show_secret(username):
    """Show hidden page for logged-in users only."""
    # breakpoint()
    # if "username" not in session:
    #     flash("You must be logged in to view!")
    #     return redirect("/")

    if session['username'] != username:
        flash("You are not authorized to view this page!")
        return redirect("/")
    else:
        user = User.query.get_or_404(username)
        form = CSRFProtectForm()
        return render_template("secret.html", user=user, form=form)


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "username" if present, but no errors if it wasn't
        session.pop("username", None)
        # breakpoint()

    return redirect("/")


###################### NOTES ###################################

@app.post("/users/<username>/delete")
def delete_user(username):
    """Checks user for authorization to delete, on success redirect to register,
    if fail, redirects to login"""

    form = CSRFProtectForm()

    if form.validate_on_submit():

        if "username" not in session:
            flash("You must be logged in to view!")
            return redirect("/login")
        elif session['username'] != username:
            flash("You are not authorized!")
            return redirect("/")
        else:
            user = User.query.get_or_404(username)
            db.session.delete(user)
            db.session.commit()
            session.pop("username", None)
            flash("User has been deleted")
            return redirect('/')

    return redirect("/login")


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note(username):
    """ Goes to add note page, on submission, creates not and redirects back to
    user page to show all current user notes, on failure, renders add note page
    """

    form = CreateNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title,
                    content=content,
                    owner=username)
        # TODO: do we need to authorize every single time we do something?
        # authenticate once
        db.session.add(note)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        return render_template('add_note.html', form=form, username=username)
