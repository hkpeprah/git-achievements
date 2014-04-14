# Add here specific settings for your instance of GitAchievemeents.  You should keep
# the information in here private and avoid adding it your repository (especially if
# it's public) if at all possible.  You can override common settings in here as well.
from common import *

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
