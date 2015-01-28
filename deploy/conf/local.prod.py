import os
from server.conf.default import *

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${db_name}',
        'USER': '${db_username}',
        'PASSWORD': '${db_password}',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}

CONN_MAX_AGE = 10


SECRET_KEY = '${djangokey}'

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

DEBUG = False
