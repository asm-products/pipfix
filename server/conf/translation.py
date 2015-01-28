import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))))

LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'locale'), )

LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True