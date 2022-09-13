import os

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from server import db, db_name, default_admin_username, default_admin_password


class admin_user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable = False, unique = True)
    password = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return "<Acticle {}>".format(self.id)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable = False, unique = True)
    password = db.Column(db.String(200), nullable = False)
    token = db.Column(db.String(40))
    dateRegistered = db.Column(db.String(120))
    activated = db.Column(db.String(5))

    def __repr__(self):
        return "<Acticle {}>".format(self.id)

class flip_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filesDirectoryID = db.Column(db.Integer)
    views = db.Column(db.Integer, default = 0)
    password = db.Column(db.Text)
    userID = db.Column(db.Integer)
    brand = db.Column(db.String(30))
    external_download = db.Column(db.String(5))
    flip_book_id = db.Column(db.Integer)
    disable_right_click = db.Column(db.String(5))

    def __repr__(self):
        return "<Acticle {}>".format(self.id)

# this table need for generate unquee file directory id
class current_directory_id(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unQueeFilesDirectoryID = db.Column(db.Integer)

    def __repr__(self):
        return "<Acticle {}>".format(self.id)


# if here is not database then create
if not os.path.exists( os.path.join(os.path.abspath(os.path.dirname(__file__)), '{}.db'.format(db_name)) ):
    db.create_all()
    # set default admin username/password
    user = admin_user(username = default_admin_username, password = generate_password_hash(default_admin_password))
    first_directory_id = current_directory_id(unQueeFilesDirectoryID = 1)
    db.session.add(user)
    db.session.add(first_directory_id)
    db.session.commit()
