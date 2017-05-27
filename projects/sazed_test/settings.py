from os.path import abspath
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import normpath
from sys import path

PROJECT_PATH = dirname(abspath(__file__))
PROJECT_NAME = basename(PROJECT_PATH)
PROJECTS_PATH = normpath(join(PROJECT_PATH, '..'))

APPLICATIONS_PATH = normpath(join(PROJECTS_PATH, '../applications'))
DATABASES_PATH = normpath(join(PROJECTS_PATH, '../databases'))
CONFIGURATION_PATH = normpath(join(PROJECTS_PATH, '../configuration'))
STATIC_PATH = normpath(join(PROJECTS_PATH, '../static'))

path.insert(0, APPLICATIONS_PATH)
path.insert(0, PROJECTS_PATH)

# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

ALLOWED_HOSTS = []

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    #{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    #{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    #{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    #{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(DATABASES_PATH, PROJECT_NAME + '.sqlite3'),
        'ATOMIC_REQUESTS': True
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sazed',
    'sazed_test'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

SECRET_KEY = 'h9&mw-x%q0^z$x0snjdxnq2!0h0odqyoj8f%giia=$(-)gy!r4'
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = False
X_FRAME_OPTIONS = 'DENY'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

DATE_FORMAT = 'Y-M-d'
DATETIME_FORMAT = 'Y-M-d H:i:s'
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = STATIC_PATH

TEMPLATES = [
    {
        'OPTIONS':
        {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ]
        },
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True
    }
]

DEBUG = True
