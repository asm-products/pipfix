import os

DJANGO_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'client'),
)

TEMPLATE_DIRS = (
    os.path.join(DJANGO_ROOT, 'templates'),
)