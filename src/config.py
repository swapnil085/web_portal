# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Application threads
# A common general assumption is using 2 per available cores
# to handle incoming requests using one
# perform backgorund operations using the other
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure and unique secret key for signing the data
CSRF_SESSION_KEY = 'secret'

# Secret key for signing cookies
SECRET_KEY = 'secret'

# define database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/automation'

SQLALCHEMY_TRACK_MODIFICATIONS = False