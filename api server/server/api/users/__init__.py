# describe the methods for user column

import shutil
from datetime import datetime
from random import randint

from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for, request
from flask_mail import Message

from server import db, secret_key, FLIP_BOOK_FILES_DIRECTORY, mail
from server.database import flip_book, user
from server.api.flip_book import get_user_flip_books


def generate_token(username = 'username',password_hash = 'password_hash',secret_key = 'secret_key'):
    return generate_password_hash(username + password_hash + secret_key)

def get_all_users():
    users = []
    for user in db.engine.execute('SELECT * FROM `user`'):
        id = user[0]
        date = user[4]
        username = user[1]
        activated = user[5]

        flip_books = flip_book.query.filter_by(userID = id).count()
        users.append({ 'id': str(id), 'registered': date, 'username': username, 'flip_books_count': str(flip_books), 'activated': activated})
    return users


def get_user_info(id,domain):
    user_info = user.query.filter_by(id=id).first()
    if not user_info: return {}
    user_info.flip_books = get_user_flip_books(id,domain)
    return user_info

def create_new_user(username,password, user_active):
    password_hash = generate_password_hash(password)
    time_registered = str(datetime.now().strftime('%Y-%m-%d %H:%M'))
    token = generate_token(secret_key = secret_key, password_hash = password_hash, username = username)
    db.engine.execute('INSERT INTO `user` (`username`, `password`, `token`, `dateRegistered`, `activated`) VALUES (?,?,?,?,?)',
                      [username, password_hash, token, time_registered, user_active])
    return token

def delete_user(id):
    directory_ids = db.engine.execute('SELECT `filesDirectoryID` FROM `flip_book` WHERE `userID` = ?', [id])
    for directory_id in directory_ids:
        directory_id = directory_id[0]
        shutil.rmtree(f'{FLIP_BOOK_FILES_DIRECTORY}/{directory_id}')
    db.engine.execute('DELETE FROM `flip_book` WHERE `userID` = ?', [id])
    db.engine.execute('DELETE FROM `user` WHERE `id` = ?', [id])



def get_user_id_by_token(token):
    users = user.query.filter_by(token = token, activated = "true").all()
    if not users: return None
    return users[0].id


def get_token_by_user_info(username,password):
    users = user.query.filter_by(username = username).all()
    if not users: return None
    selected_user = users[0]
    if check_password_hash(selected_user.password, password):
        return selected_user.token
    return None


def has_email_account(username):
    if not user.query.filter_by(username = username).all(): return False
    return True

def generate_new_password_user(email):
    # generate new password save it to user and return
    dictionary = 'abcdefghijklmnopqrstuvwxyz1234567890'
    new_password = ''
    for i in range(12):
        if randint(1,2) == 1:
            new_password += dictionary[randint(0, len(dictionary) - 1)].lower()
        else:
            new_password += dictionary[randint(0, len(dictionary) - 1)].upper()

    password_hash = generate_password_hash(new_password)
    db.engine.execute('UPDATE `user` SET `password` = ? WHERE `username` = ?', [password_hash, email])
    return new_password

def find_user(username,token):
    if not user.query.filter_by(username = username, token = token).all(): return False
    return True

def activate_user(username,token):
    db.engine.execute('UPDATE `user` SET `activated` = "true" WHERE `username` = ? AND `token` = ?', [username, token])


def send_confirm_email(email):
    activate_link = F'{request.url_root}/confirm-page?email={email}'
    msg = Message('Please confirm your account in our service', recipients = [email])
    msg.html = f"<h3>Click to this link to activate your account </h3> </br> <a href='{activate_link}'> Activate account </a>"
    mail.send(msg)

def send_password_email(email,new_password):
    msg = Message('Changed password in our service!', recipients = [email])
    msg.html = f"Somebody or you changed for your account the password, current password for the account is {new_password}, If it wasn't you, please contact with admin"
    mail.send(msg)
