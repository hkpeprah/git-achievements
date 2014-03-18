from django.conf import settings
from django.db.models import get_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured


class UserProfileModelBackend(ModelBackend):
    """
    Custom backend that grabs our UserProfile by default instead of Django's
    default Auth User.
    """

    def authenticate(self, username=None, password=None):
        """
        Authenticates the user.

        @param self: UserProfileModelBackend instance
        @param username: User's name
        @param password: User's password
        """
        try:
            user = self.user_class.objects.get(username=username)
 
            if user.check_password(password):
                return user

        except self.user_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Gets the UserProfile instead of the default user.

        @param self: UserProfileModelBackend instance
        @param user_id: ID of the user
        @return: UserProfile
        """
        try:
            return self.user_class.objects.get(pk=user_id)
        except serlf.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        """
        Returns the custom user class that is being used.
        """
        if not hasattr(self, '_user_class'):
            print settings.CUSTOM_USER_MODEL
            print get_model('app.assets.models.UserProfile')
            print get_model('app.assets.mdoels.achievement_models.UserProfile')

            self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))

            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model.')

        return self._user_class
