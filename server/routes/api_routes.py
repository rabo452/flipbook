import json

from flask import request

from server import app, allowed_file_types, mail
from server.api.users import create_new_user, get_user_id_by_token, get_token_by_user_info, has_email_account, \
    generate_new_password_user, find_user, activate_user, send_confirm_email, send_password_email
from server.api.flip_book import upload_file_to_server, has_password_flip_book, is_right_password_flip_book, \
    has_flip_book, get_flip_book_info, increase_flip_book_views


@app.route('/api/create-flip-book', methods=['POST'])
def api_create_flip_book():
    try:
        try:
            file_data = request.files['file'].read()
        except:
            # it's google docs link
            file_data = ''

        google_docs_link = request.form['google_docs']
        password = request.form['flip_book_password']
        external_download = request.form['external_download']
        brand = request.form['brand']
        disable_right_click = request.form['disable_right_click']
        logo_file_data = request.files['logo'].read()

        user_id = get_user_id_by_token(request.form['token'])
        if not user_id:
            return json.dumps({'message': "User token doesn't valid"})

        # it's google docx upload
        if google_docs_link != '':
            page_id = upload_file_to_server(file_data, logo_file_data, brand, external_download, disable_right_click,
                                            None, google_docs_link, password=password, user_id=user_id)
            return json.dumps({'page_id': page_id})

        if not file_data:
            return json.dumps({'page_id': None, 'message': "User didn't upload the file"})

        # upload original file
        for type in allowed_file_types:
            if type in request.files['file'].content_type:
                # docx format
                if 'vnd.openxmlformats-officedocument' in type:
                    page_id = upload_file_to_server(file_data, logo_file_data, brand, external_download,
                                                    disable_right_click, 'docx', password=password, user_id=user_id)
                else:
                    page_id = upload_file_to_server(file_data, logo_file_data, brand, external_download,
                                                    disable_right_click, type, password=password, user_id=user_id)
                return json.dumps({'page_id': page_id})

        return json.dumps({'page_id': None, 'message': 'User uploaded the not allowed file to server'})
    # TODO: create for each exception own branch of except
    except:
        return json.dumps({'page_id': None, 'message': 'External error'})


# register account, not activated
@app.route('/api/register-user', methods=['POST'])
def api_send_activation():
    try:
        email = request.form['email']
        password = request.form['password'].replace(' ', '')
        send_confirm_email(email)

        token = create_new_user(email, password, 'false')
        return json.dumps({'token': token})
    # TODO: create for each exception own branch of except
    except:
        return json.dumps({'message': 'Invalid request', 'token': ''})


@app.route('/api/login-user', methods=['POST'])
def api_login_user():
    try:
        email = request.form['email']
        password = request.form['password'].replace(' ', '')

        token = get_token_by_user_info(email, password)
        if not token: return json.dumps({'message': 'No user', 'token': ''})

        return json.dumps({'token': token})
    # TODO: create for each exception own branch of except
    except:
        return json.dumps({'message': 'Invalid request', 'token': ''})


@app.route('/api/recover-password', methods=['POST'])
def api_recover_password():
    try:
        email = request.form['email']
        if not has_email_account(email):
            return json.dumps({'success': False, 'message': "User email hasn't found"})

        new_password = generate_new_password_user(email)
        send_password_email(email, new_password)

        return json.dumps({'success': True})
    # TODO: create for each exception own branch of except
    except:
        return json.dumps({'success': False})


@app.route('/api/confirm-account', methods=['POST'])
def api_confirm_account():
    try:
        token = request.form['token']
        email = request.form['email']

        has_user = find_user(email, token)
        if not has_user:
            return json.dumps({'success': False})

        activate_user(email, token)
        return json.dumps({'success': True})
    # TODO: create for each exception own branch of except
    except:
        return json.dumps({'success': False})


@app.route('/api/has-flipbook', methods=['POST'])
def api_has_flipbook():
    try:
        id = request.form['flipbookId']
        return json.dumps({'has': has_flip_book(id)})
    # TODO: create for each exception own branch of except
    except:
        return json.dumps({'has': False})


@app.route('/api/has-flipbook-password', methods=['POST'])
def api_flipbook_password():
    try:
        id = request.form['flipbookId']
        has_password = has_password_flip_book(id)
        return json.dumps({'has_password': has_password})
    # TODO: create for each exception own branch of except
    except:
        return json.dumps({'has_password': False})


@app.route('/api/check-password', methods=['POST'])
def api_check_flip_book_password():
    try:
        id = request.form['flipbookId']
        password = request.form['password']
        return json.dumps({'password_right': is_right_password_flip_book(id, password)})
    # TODO: create for each exception own branch of except
    except:
        return json.dumps({'password_right': False})


@app.route('/api/get-flipbook', methods=['POST'])
def api_get_flipbook():
    try:
        id = request.form['flipBookId']
        password = request.form['password']

        if not is_right_password_flip_book(id, password):
            return json.dumps({})

        data = get_flip_book_info(id, 'http://' + request.headers['host'])
        increase_flip_book_views(id)

        return json.dumps(data)
    # TODO: create for each exception own branch of except
    except:
        return json.dumps({})
