# describe admin user column in db

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user

from server import db
from server.database import admin_user


def login_admin_user(username, password):
    user = admin_user.query.filter_by(username = username).first()
    if not user or not check_password_hash(user.password, password): return False
    login_user(user)
    return True

def change_admin_password(username,new_password):
    db.engine.execute('UPDATE `admin_user` SET `password` = ? WHERE `username` = ?', [generate_password_hash(new_password), username])
