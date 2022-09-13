# file for getting and saving the flip book data

import os
import re
import shutil
import base64

import fitz
import requests
from flask import url_for

from server import db, FLIP_BOOK_FILES_DIRECTORY, GOOGLE_DOCS_API_KEY, CLOUD_CONVERTER_API_KEY
from server.database import current_directory_id, flip_book


def has_flip_book(flip_book_id):
    row = flip_book.query.filter_by(flip_book_id=flip_book_id).all()
    if not row: return False
    return True


def has_password_flip_book(flip_book_id):
    row = flip_book.query.filter_by(flip_book_id=flip_book_id, password='').all()
    if not row: return True
    return False


def is_right_password_flip_book(flip_book_id, password):
    row = flip_book.query.filter_by(flip_book_id=flip_book_id, password=password).all()
    if not row: return False
    return True


def increase_flip_book_views(flip_book_id):
    row = flip_book.query.filter_by(flip_book_id=flip_book_id).one()
    views = (int(row.views) + 1)
    db.engine.execute('UPDATE `flip_book` SET `views` = ? WHERE `flip_book_id` = ?', [views, flip_book_id])


# this function delete flip book with all files
def delete_flip_book(id, directory_id):
    db.engine.execute('DELETE FROM `flip_book` WHERE `id` = ?', [id])
    shutil.rmtree(f'{FLIP_BOOK_FILES_DIRECTORY}/{directory_id}')


def get_flip_book_info(flip_book_id, domain):
    flip_book_obj = {}
    row = flip_book.query.filter_by(flip_book_id=flip_book_id).one()

    flip_book_obj['views'] = row.views
    flip_book_obj['brand'] = row.brand
    flip_book_obj['images'] = [(domain + image) for image in get_flip_book_images(row.filesDirectoryID)]
    flip_book_obj['logotype'] = domain + url_for('files', filename=f'{row.filesDirectoryID}/logo_image/logo.jpg')
    flip_book_obj['text_pages'] = get_text_pages(row.filesDirectoryID)
    flip_book_obj['disable_right_click'] = row.disable_right_click
    flip_book_obj['links'] = [list(set([link for link in re.findall(r'https?:\/\/\S+\b', text_page) if len(link) > 12]))
                              for text_page in flip_book_obj['text_pages']]
    if row.external_download == "true":
        flip_book_obj['external_file_link'] = domain + url_for('files', filename=(
                f'{row.filesDirectoryID}/external_file/' +
                os.listdir(os.path.join(FLIP_BOOK_FILES_DIRECTORY, f'{row.filesDirectoryID}/external_file/'))[0]))
    else:
        flip_book_obj['external_file_link'] = ''

    return flip_book_obj


def get_text_pages(directory_id):
    text_pages = []

    directory = os.path.join(FLIP_BOOK_FILES_DIRECTORY, f'{directory_id}/flip_book_text/')
    i = 1
    while True:
        if not os.path.exists(os.path.join(FLIP_BOOK_FILES_DIRECTORY, f'{directory_id}/flip_book_text/{i}.txt')): break

        f = open(os.path.join(FLIP_BOOK_FILES_DIRECTORY, f'{directory_id}/flip_book_text/{i}.txt'), 'rb')
        text_pages.append(f.read().decode('utf-8', errors='ignore'))
        f.close()
        i += 1

    return text_pages


def get_user_flip_books(user_id, domain):
    flip_books = []
    for row in db.engine.execute('SELECT * FROM `flip_book` WHERE `userID` = ?', [user_id]):
        try:
            flip_book = {}
            flip_book['views'] = row[2]
            flip_book['filesDirectoryID'] = row[1]
            flip_book['id'] = row[0]
            flip_book['link'] = f'{domain}flipbook?id={row[7]}'
            flip_book['brand'] = row[5]
            flip_book['external_download'] = row[6]
            flip_book['disable_right_click'] = row[8]
            flip_book['logotype'] = url_for('files', filename=f'{row[1]}/logo_image/logo.jpg')

            if not row[3]:
                flip_book['password'] = 'False'
            else:
                flip_book['password'] = row[3]

            flip_book['images'] = get_flip_book_images(str(flip_book['filesDirectoryID']))
            flip_book['external_file'] = url_for('files', filename=(f'{row[1]}/external_file/' + os.listdir(
                os.path.join(FLIP_BOOK_FILES_DIRECTORY, f'{row[1]}/external_file/'))[0]))
            flip_books.append(flip_book)
        except:
            continue  # files can be deleted by admin or server, and it'd raise error

    return {
        'flip_books': flip_books,
        'count': len(flip_books)
    }


def get_flip_book_images(directory_id):
    files = []

    # get images by order
    i = 1
    while True:
        if not os.path.exists(os.path.join(FLIP_BOOK_FILES_DIRECTORY, f'{directory_id}/images/{i}.jpg')): break
        files.append(url_for('files', filename=f'{directory_id}/images/{i}.jpg'))
        i += 1

    return files


# this method save & convert to images the file that user uploaded
def upload_file_to_server(file_data, logo_file_data, brand, external_download, disable_right_click, file_extension=None,
                          google_pdf_url='', password='', user_id=1):
    directory_id = current_directory_id.query.filter_by(id=1).first().unQueeFilesDirectoryID

    image_download_directory = os.path.join(FLIP_BOOK_FILES_DIRECTORY, f'{directory_id}/images/')
    text_download_directory = os.path.join(FLIP_BOOK_FILES_DIRECTORY, f'{directory_id}/flip_book_text/')
    external_file_download_directory = os.path.join(FLIP_BOOK_FILES_DIRECTORY, f'{directory_id}/external_file/')
    user_logo_directory = os.path.join(FLIP_BOOK_FILES_DIRECTORY, f'{directory_id}/logo_image/')

    try:
        if not os.path.exists(image_download_directory): os.makedirs(image_download_directory)
        if not os.path.exists(text_download_directory): os.makedirs(text_download_directory)
        if not os.path.exists(external_file_download_directory): os.makedirs(external_file_download_directory)
        if not os.path.exists(user_logo_directory): os.makedirs(user_logo_directory)

        # convert google docx to pdf
        if google_pdf_url != '':
            generated_pdf = True
            file_extension = 'pdf'
            file_path = generate_docx_from_google_docx(google_pdf_url, external_file_download_directory)
            file_path = generate_pdf_by_docx(file_path, external_file_download_directory)
        else:
            generated_pdf = False
            file_path = os.path.join(external_file_download_directory, f'file.{file_extension}')
            f = open(file_path, 'wb')
            f.write(file_data)
            f.close()

            if file_extension in 'docx':
                generated_pdf = True
                file_extension = 'pdf'
                file_path = generate_pdf_by_docx(file_path, external_file_download_directory)

        # create images for each page extension that user uploaded and generate text for each page of flip book
        if file_extension in ['jpg', 'png', 'jpeg']:
            # if user uploaded image, the flip book will contain only this image
            f = open(os.path.join(image_download_directory, '1.jpg'), 'wb')
            f.write(file_data)
            f.close()
        elif file_extension in 'pdf':
            generate_images_text_by_pdf(file_path, image_download_directory, text_download_directory)
            if generated_pdf: os.remove(file_path)  # delete the generated pdf from external file

        # save logo file
        f = open(os.path.join(user_logo_directory, 'logo.jpg'), 'wb')
        f.write(logo_file_data)
        f.close()

        # save flipbook into database
        db.engine.execute(
            'INSERT INTO `flip_book` (`filesDirectoryID`, `views`, `password`, `userID`, `brand`, `external_download`,`flip_book_id`, `disable_right_click`) VALUES (?,?,?,?,?,?,?,?)',
            [directory_id, 0, password, int(user_id), brand, external_download, int(directory_id), disable_right_click])
        change_uninque_directory_id(directory_id)
        return directory_id
    # TODO: create for each exception own branch of except
    except:
        shutil.rmtree(os.path.join(FLIP_BOOK_FILES_DIRECTORY, str(directory_id)))
        return None


# user can upload file by indicating the google pdf link
def generate_docx_from_google_docx(url, download_dir):
    file_id = re.findall(r'/d/([\S]+)/', url)[0]  # get file id

    r = requests.get(f'https://docs.google.com/document/d/{file_id}/export?format=doc&key={GOOGLE_DOCS_API_KEY}')
    f = open(os.path.join(download_dir, 'file.docx'), 'wb')
    f.write(r.content)
    f.close()

    return os.path.join(download_dir, 'file.docx')


def generate_pdf_by_docx(file_path, download_dir):
    f = open(file_path, 'rb')
    binary = f.read()
    f.close()

    # convert docx to pdf by external api cloudconvert
    url = 'https://api.cloudconvert.com/convert'
    data = {
        "apikey": CLOUD_CONVERTER_API_KEY,
        "inputformat": "docx",
        "outputformat": "pdf",
        "input": "base64",
        "wait": "true",
        "download": "inline",
        "file": base64.b64encode(binary),
        'filename': 'example.docx'
    }
    r = requests.post(url, data=data)

    f = open(os.path.join(download_dir, 'file.pdf'), 'wb')
    f.write(r.content)
    f.close()

    return os.path.join(download_dir, 'file.pdf')


# generate images and text for pdf file and store it in image dir and text dir
def generate_images_text_by_pdf(file_path, image_dir, text_dir):
    pages = fitz.open(file_path)

    # generate images and text page by page
    for i in range(len(pages)):
        page = pages[i]
        page.get_pixmap().save(os.path.join(image_dir, f'{i + 1}.jpg'))

        text = page.get_text()
        f = open(os.path.join(text_dir, f'{i + 1}.txt'), 'w+', encoding='utf-8')
        f.write(text)
        f.close()


# update uninquee directory id
def change_uninque_directory_id(current_id):
    uninquee_id = current_id + 1
    db.engine.execute(
        'UPDATE `current_directory_id` SET `unQueeFilesDirectoryID` = ? WHERE `unQueeFilesDirectoryID` = ?',
        [uninquee_id, current_id])
