import os

db_name = 'app'
default_admin_username = 'admin'  # this is first username/password of admin when you're logged
default_admin_password = 'admin'

secret_key = 'secret key fff'  # it's secret key for admin authorization and static salt for password in db

FLIP_BOOK_FILES_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)), "files")
allowed_file_types = ['jpg', 'jpeg', 'png', 'pdf',
                      'vnd.openxmlformats-officedocument']  # vnd.openxmlformats-officedocument - docx
GOOGLE_DOCS_API_KEY = ''

EMAIL_SERVER = 'smtp.gmail.com'  # here the email settings, without these users can't sign up with your app
EMAIL_PORT = 465
EMAIL_USERNAME = ''
EMAIL_PASSWORD = ''

# https://cloudconvert.com/
CLOUD_CONVERTER_API_KEY = ""  # this api for cloud convert the .docx => .pdf
