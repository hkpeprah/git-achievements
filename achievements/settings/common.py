"""
Django settings for achievements project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import django.conf.global_settings as DEFAULT_SETTINGS


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '369p)5nle)!r*4jybx)7nx2-1vl9p*q=g$ej*6^$l4@v6p*f2e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Template specifications
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Add custom apps here
    'app.assets',
    'app.achievement',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
ROOT_URLCONF = 'achievements.urls'
WSGI_APPLICATION = 'achievements.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)


# Example project settings
# Override this attributes with your own as needed or make use of
# the various applications that provide functionality for these things
CONTRIBUTORS = (
    {
        'username': "hkpeprah",
        'name': "Ford",
        'email': "ford.peprah@uwaterloo.ca",
        'image': "https://2.gravatar.com/avatar/a5c900cba2a92e5a715a8e37c5827860?d=https%3A%2F%2F \
            identicons.github.com%2F79a82506f16a92c3970e02229005157f.png",
        'rank': 1,
        'service': "Github",
        'points': 9001
    },
    {
        'username': "nt3rp",
        'name': "Nicholas Terwoord",
        'email': "nicholas.terwoord+code@gmail.com",
        'image': "https://1.gravatar.com/avatar/b6cb96321f0d40e7d2aecce9f6037335?d=https%3A%2F%2F \
            identicons.github.com%2F8231e02ad9e8519dd31182f2d6a68fa2.png",
        'rank': 2,
        'service': "Github",
        'points': 8999
    },
    {
        'username': "1337",
        'name': "Brian L",
        'email': "brian@ohai.ca",
        'image': "https://1.gravatar.com/avatar/22439d590eb5c6a3f191fff4f4d655fc?d=https%3A%2F%2F \
            identicons.github.com%2F03800e8f5cc22057868bfa9b2e9b3571.png",
        'rank': 3,
        'service': "Github",
        'points': 1337
    },
)

ACHIEVEMENTS = (
    {
        'name': "Homer Simpson",
        'description': "Submit a pull request that fails to pass Jenkins unit tests at least once.",
        'difficulty': "easy",
        'count': 3,
        'title': {
            'name': "Homer",
            'difficulty': "easy"
        }
    },
    {
        'name': "Baby Steps",
        'description': "Submit your first pull request.",
        'difficulty': "easy",
        'count': 3,
        'title': {
            'name': "Look at me mom!",
            'difficulty': "easy"
        }
    },
    {
        'name': "Push Level 1",
        'description': "Push five(5) or more commits to a single branch.",
        'difficulty': "easy",
        'count': 3,
        'tilte': None
    },
    {
        'name': "Over 9000",
        'description': "Submit a pull request with over 9000 changes made, additions or deletions, and have it merged into the development branch.",
        'difficulty': "very-hard",
        'count': 0,
        'title': {
            'name': "Goku",
            'difficulty': "very-hard"
        }
    }
)

CAROUSEL = (
    {
        'image': "http://lorempixel.com/1920/1080/technics/",
        'title': "First Slide",
        'text': "Sample text for the first slide."
    },
    {
        'image': "http://lorempixel.com/1920/1079/technics/",
        'title': "Second Slide",
        'text': "Sample text for the second slide."
    },
    {
        'image': "http://lorempixel.com/1920/1078/technics/",
        'title': "Third Slide",
        'text': "Sample text for the third slide."
    },
)

BASIC_EXAMPLE_CONFIG = {
    'titles': (
        {
            'name': "Homer",
            'difficulty': "easy"
        },
        {
            'name': "The Pusher",
            'difficulty': "medium"
        },
        {
            'name': "Stan Darsh",
            'difficulty': "hard"
        },
        {
            'name': "The Nuker",
            'difficulty': "very-hard"
        },
        {
            'name': "Open-Source Champ",
            'difficulty': "impossible"
        },
    )
}
