"""
Django settings for Git-Achievements project.

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

# Bro, keep the secret key used in production secret!
SECRET_KEY = '369p)5nle)!r*4jybx)7nx2-1vl9p*q=g$ej*6^$l4@v6p*f2e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Fixture directions, where Django looks for initial data to populate
# the database with
FIXTURE_DIRS = (
    'app/achievement/fixtures/',
)

# Paths for the loaddata script to load in data to populate the database
# Loads in order to allow dependencies be satisfied
FIXTURE_PATHS = (
    'app/achievement/fixtures/badges.json',
    'app/achievement/fixtures/qualifiers.json',
    'app/achievement/fixtures/quantifiers.json',
    'app/achievement/fixtures/methods.json',
    'app/achievement/fixtures/difficulties.json',
    'app/achievement/fixtures/badges.json',
    'app/achievement/fixtures/conditions.json',
    'app/achievement/fixtures/achievements.json',
    # These two must come in this order and be the
    # last in the tuple
    'app/achievement/fixtures/achievementcondition.json',
    'app/achievement/fixtures/users.json',
)

# Authentication backends
# Provides the means by which users can authenticate and login
AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.bitbucket.BitbucketOAuth',
    'social.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Template specifications
# Process and set settings for templates, as well as load
# templates.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    # Third party processors
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    # Custom processors
    'gitachievements.context_processors.hosting_services',
    # Request proccessor
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


# Application definition
INSTALLED_APPS = (
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party applications
    'social.apps.django_app.default',
    'tastypie',
    'south',
    # Add custom apps here
    'app.services',
    'app.achievement',
)

# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
ROOT_URLCONF = 'gitachievements.urls'
WSGI_APPLICATION = 'gitachievements.wsgi.application'


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

# Tastypie Default Format
TASTYPIE_DEFAULT_FORMATS = ['json']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "gitachievements/static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'

# Social Authentication Settings
# Settings for the Django Pipeline
SOCIAL_AUTH_LOGIN_URL = '/login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/profile/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/profile/'
SOCIAL_AUTH_ENABLED_BACKENDS = ('github', )
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'services/auth/signup.html'
# The pipeline determins how a user is processed after having
# authenticated with OAuth
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    # Custom method for populating data fields for the
    # user.  At this point it's assumed we have a user object.
    'app.achievement.utils.populate_profile_fields',
    # Continue normal pipeline
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
# Github application settings
SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''

# Additional settings
# An achievement approval threshold of 0 is infinite, which means that only
# moderators/admins can approve achievements.  Override in your custom settings
# to set a threshold that will allow achievements to be automatically approved when
# they reach a certain amount.
ACHIEVEMENT_APPROVAL_THRESHOLD = 0
# Override this with "True" if you're running a local/team instance
IS_ORGANIZATION = False
# This is where we fetch the project contributors from
CONTRIBUTORS_URL = "https://api.github.com/orgs/git-achievements/public_members"
# This tuple should contain a list of the services that you wish
# to have support for.
HOSTING_API_SERVICES = (
    'Github',
)
