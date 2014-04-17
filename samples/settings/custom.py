# Add here specific settings for your instance of GitAchievemeents.  You should keep
# the information in here private and avoid adding it your repository (especially if
# it's public) if at all possible.  You can override common settings in here as well.
from common import *

# It is a security concern to be running DEBUG in production, so we have to make sure
# to turn it off; it also avoids printing out our source code and debug statements
import os

DEBUG = False
TEMPLATE_DEBUG = False

# Set this to false if you're not running an organization/group instance (if you're not,
# why not use Git Achievement's git-achievements?)
IS_ORGANIZATION = True

# Put in your github application authentication key and secret.  This lets
# the application authenticate users.  To find out how to generate a secret
# key and authentication key, see register a new application to generate these
# credentials here: https://github.com/settings/applications/new
SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''

# You need to generate a new secret key to use.  If you already have one, you
# can input it here, otherwise you can generate the key by running the add_new_key
# script in the bin directory.
SECRET_KEY = ''

# To serve the Django Application on the web server we use Gunicorn managed through
# passenger, so we have to add it to the list of available applications
# Add gunicorn to the list of available applications
INSTALLED_APPS += (
    'gunicorn',
)

# Next we specify the database.  In the web server we run a PostgreSQL database, so
# you'll have to create a user to use with the database if you don't already have one.
# Instructions for doing so can be found here
# https://www.digitalocean.com/community/articles/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn
DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3', or 'oracle'
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # These settings are not used with SQlite
        'NAME': 'achievements',
        'PASSWORD': '', # choose a password here
        'HOST': '', # host is empty because we bind to localhost
    }
}

# A list of strings representing the host/domain names that this Django site can serve. This is a
# security measure to prevent an attacker from poisoning caches and password reset emails with 
# links to malicious hosts by submitting requests with a fake HTTP Host header, which is possible 
# even under many seemingly-safe web server configurations.
# Replace this with your host
ALLOWED_HOSTS = (
    '.git-achievements.com',
)
