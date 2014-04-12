from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

# Database
}BASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'repylia',
        'USER': 'repylia',
        'PASSWORD': 'tyranosaure',
        'HOST': 'localhost',
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
