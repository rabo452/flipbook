import json

from flask import url_for, request, render_template, redirect, send_from_directory
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user

from server import app, FLIP_BOOK_FILES_DIRECTORY
from server.api.users import get_all_users, get_user_info, delete_user, create_new_user
from server.api.admin_user import login_admin_user, change_admin_password
from server.api.flip_book import delete_flip_book


@app.route('/admin-login', methods=['GET', 'POST'])
def log_in_page():
    if request.method == 'GET': return render_template('/admin/admin_login.html')
    if request.method == 'POST':
        # request from login form
        username = request.form['username']
        password = request.form['password']

        if not login_admin_user(username, password): return render_template('/admin/admin_login.html', error='The username or password is wrong')
        return redirect(url_for('admin_page'))


@app.route('/administrator', methods=['GET'])
@login_required
def admin_page():
    users = get_all_users()
    return render_template('/admin/admin_panel.html', users = users)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout_page():
    logout_user()
    return "You logged out"


@app.route('/change-password', methods=['POST', 'GET'])
@login_required
def change_password_page():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['new_password']
        change_admin_password(username,password)
        return redirect(url_for('admin_page'))
    else:
        return render_template('/admin/admin_change_pas.html')


# the route for files directory
@app.route('/files/<path:filename>')
def files(filename):
    return send_from_directory(FLIP_BOOK_FILES_DIRECTORY, filename)


@app.route('/create-user')
@login_required
def create_user_page():
    return render_template('/admin/create_user_page.html')

@app.route('/delete-user', methods=['POST'])
@login_required
def delete_user_page():
    user_id = request.form['user_id']
    delete_user(user_id)
    return 'user successfully deleted'

@app.route('/flip-book-delete', methods=['POST'])
@login_required
def flip_book_delete_page():
    flip_book_id = request.form['flip_book_id']
    directiory_id = request.form['directory_id']
    delete_flip_book(flip_book_id, directiory_id)
    return 'Done'

@app.route('/user/<int:user_id>')
@login_required
def user_page(user_id):
    user = get_user_info(int(user_id), request.url_root)
    if not user: return 'User not found'
    return render_template('/admin/user_details_page.html', user = user)


@app.route('/admin-create-user', methods = ['POST'])
@login_required
def register_user():
    try:
        username = request.form['username']
        password = request.form['password']
        if (len(username) < 7) or (len(password) < 7): return json.dumps({'token': ''})

        token = create_new_user(username, password, 'true')
        return json.dumps({'token': token})
    except:
        return json.dumps({'token': ''})
