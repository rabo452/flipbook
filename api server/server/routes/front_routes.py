# routes for front-end part of project

from flask import url_for, render_template, request

from server import app


@app.route('/', methods = ['GET'])
def index_page():
    return render_template('/front-end/index.html')

@app.route('/login', methods = ['GET'])
def login_page():
    return render_template('/front-end/login.html')

@app.route('/forgot', methods = ['GET'])
def forgot_page():
    return render_template('/front-end/forgot.html')

@app.route('/flipbook', methods = ['GET'])
def flipbook_page():
    try:
        id = request.args.get('id')
        facebook_logo_image_url = request.url_root + url_for('files', filename=f'{id}/logo_image/logo.jpg')
        return render_template('/front-end/flipbook.html', facebook_logo_image_url = facebook_logo_image_url)
    except:
        return render_template('/front-end/flipbook.html', facebook_logo_image_url = '')

@app.route('/confirm-page', methods = ['GET'])
def confirm_page():
    return render_template('/front-end/confirm-page.html')
