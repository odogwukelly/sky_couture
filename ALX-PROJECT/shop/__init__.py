# Import necessary Flask and extension modules
from flask import Flask
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager
from flask_msearch import Search



# Define the base directory for the application
basedir = os.path.abspath(os.path.dirname(__file__))
# Create a Flask application instance
app = Flask(__name__)
# Configure settings for file uploads
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
# Set a secret key for the application (used for sessions and security)
app.config['SECRET_KEY'] = 'fhjjgj4567jgfgd67fsdsx123cxcvnkl'
# Define an UploadSet for uploaded photos
photos = UploadSet('photos', IMAGES)
# Configure file uploads for the app using Flask-Uploads
configure_uploads(app, photos)


# Initialize a SQLAlchemy database instance
db = SQLAlchemy(app)
# Initialize a Bcrypt instance for password hashing
bcrypt = Bcrypt(app)
# Initialize a Flask-MSearch instance for searching functionality
search = Search()
search.init_app(app)

# Initialize a Flask-Login manager for user authentication
login_manager = LoginManager()
login_manager.init_app(app)

# Set the login view, message category, and login message
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
login_manager.login_message = u"Please login first"




# Import routes from other modules within the application
from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customer import routes
