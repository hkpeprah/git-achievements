from app.services.utils import json_response
from app.achievement.utils import find_nested_json
from app.achievement.hooks import check_for_unlocked_achievements


class EventData(object):
    """
    EventData emulates a dictionary while also providing convenience methods
    for accessing common attributes of service responses.
    """
    USER_KEYS = (
        'comment.user.login',
        'login',
        'username',
        'author.login',
        'author.username',
        'creator.login',
        'creator.username',
        'sender.login',
    )

    USER_KEY_PATTERNS = {
        'follow': 'target.login',
        'fork': 'forkee.owner.login',
        'issues': {
            'closed': 'issue.closed_by.login',
            'default': 'issue.user.login'
        },
        'member': 'member.login',
        'page_build': 'build.pusher.login',
        'pull_request': {
            'opened': 'pull_request.user.login',
            'default': 'sender.login'
        },
        'push': 'commits.author.username',
        'release_event': 'release.author.login',
        'team_add': 'user.login'
    }

    def __init__(self, event_type, *args, **kwargs):
        self.payload = kwargs
        # Find the individual aspects of a payload.  These vary depending on
        # the hook that was triggered.
        self.user = None
        key_pattern = EventData.USER_KEY_PATTERNS.get(event_type, None)

        if key_pattern is not None:
            # If a key pattern exists, find the user using that key
            # pattern
            if isinstance(key_pattern, str):
                user = find_nested_json(kwargs, key_pattern.split('.'))
                if isinstance(user, list):
                    self.user = user[0]
                elif user:
                    self.user = user
            else:
                key_pattern = key_pattern.get(kwargs.get('action', ''), key_pattern['default'])
                user = find_nested_json(kwargs, key_pattern.split('.'))
                if user:
                    self.user = user[0] if isinstance(user, list) else user

        # Ensure we got a user object, otherwise try to find one using
        # a generic key list of potential user locations
        if self.user is None:
            user_keys = list(EventData.USER_KEYS) + list(event_type + '.user.login')
            for user_key in user_keys:
                self.user = find_nested_json(kwargs, user_key.split('.'))
                if self.user is not None:
                    break

    def __len__(self):
        return len(self.payload)

    def __getitem__(self, key):
        return self.payload.get(key)

    def __setitem__(self, key, value):
        self.payload.set(key, value)

    def __delitem__(self, key):
        del self.payload[key]

    def __iter__(self):
        return self.payload.keys()

    def __contains__(self, item):
        return item in self.payload

    def get(self, key, default):
        return self.payload.get(key, default)


class GithubHook():
    """
    Receiever for the Github Webhooks API.
    """
    @classmethod
    def process_event(cls, event_name, event):
        """
        Processes a hook service event from Github.
        """
        # Create the Event object as a convenience
        event = EventData(event_name, **event)
        unlocked = []
        if event.user is not None:
            unlocked = check_for_unlocked_achievements(event_name, event, event.user)

        return json_response(unlocked)
