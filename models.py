"""Models for  app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Playlist."""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         nullable=False,
                         primary_key=True)
    password = db.Column(db.String(100),
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    notes = db.relationship('Note',
                            backref='user')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(username=username,
                   password=hashed,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

    # @classmethod
    # def is_duplicate(cls, username, email):
    #     """takes in username and email returns true or false whether they are taken"""

    #     u
    #     # breakpoint()
    #     if user:
    #         return False
    #     else:
    #         return True


class Note(db.Model):
    """Playlist."""

    __tablename__ = "notes"

    id = db.Column(db.Integer,
                   nullable=False,
                   autoincrement=True,
                   primary_key=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    owner = db.Column(db.String(20),
                      db.ForeignKey('users.username'),
                      nullable=False)
