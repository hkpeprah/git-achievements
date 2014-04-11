from app.services.utils import json_response
from app.achievement.utils import find_nested_json
from app.achievement.hooks import check_for_unlocked_achievement


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
        'sendor.login',
    )

    def __init__(self, event_type, *args, **kwargs):
        self.payload = kwargs
        # Find the individual aspects of a payload.  These vary depending on
        # the hook that was triggered.
        self.user = None
        if "_comment" in event_type:
            self.user = kwargs['comment']['user']['login']
            self.body = kwargs['comment']['body']
            self.url = kwargs['comment']['url']
        elif event_type == "follow":
            self.user = kwargs['target']['login']
        elif event_type == "fork":
            self.user = kwargs['forkee']['owner']['login']
            self.url = kwargs['forkee']['url']
            self.original_user = kwargs['forkee']['source']['owner']['login']
            self.original_url = kwargs['forkee']['source']['url']
        elif event_type == "issues":
            self.action = kwargs['action']
            self.user = kwargs['issue']['closed_by']['login'] if self.action == 'closed' else \
                kwargs['issue']['user']['login']
            self.url = kwargs['issue']['url']
        elif event_type == "member":
            self.user = kwargs['member']['login']
            self.action = kwargs['action']
        elif event_type == "page_build":
            self.user = kwargs['build']['pusher']['login']
            self.url = kwargs['build']['url']
        elif event_type == "pull_request":
            self.action = kwargs['action']
            self.number = kwargs['number']
            self.url = kwargs['pull_request']['url']
            self.sha = kwargs['pull_request']['head']['sha']
            if self.action == 'closed':
                self.user = kwargs['pull_request']['closed_by']['login']
            elif self.action == 'synchronize':
                self.user = kwargs['pull_request']['merged_by']['login']
            else:
                self.user = kwargs['pull_request']['user']['login']
        elif event_type == "push":
            self.sha = kwargs['head']
            self.url = kwargs['commits'][0]['url']
            self.user = kwargs['commits'][0]['author']['login']
        elif event_type == "release_event":
            self.user = kwargs['release']['author']['login']
            self.assets = kwargs['release']['assets']
            self.url = kwargs['release']['url']
        elif event_type == "status":
            self.sha = kwargs['sha']
            self.url = kwargs['target_url']
        elif event_type == "team_add":
            if 'user' in kwargs and 'login' in kwargs['user']:
                self.user = kwargs['user']['login']
            if 'repository' in kwargs:
                self.url = kwargs['repository']['url']

        # Ensure we got a user object, otherwise try to find one using
        # a generic key list of potential user locations
        if self.user is None:
            user_keys = list(USER_KEYS) + list(event_type + '.user.login')
            for user_key in user_keys:
                self.user = find_nested_json(kwargs, key.split('.'))
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

    def get(self, key):
        return self.payload.get(key)

    def get(self, key, default):
        return self.payload.get(key, default)


class GithubHook():
    """
    Receiever for the Github Webhooks API.
    """
    def process_event(headers, event):
        """
        Processes a hook service event from Github.
        """
        event_name = headers['HTTP_X_GITHUB_EVENT']
        # Create the Event object as a convenience
        event = EventData(event_name, username, **event)
        unlocked = []
        if event.user is not None:
            unlocked = check_for_unlocked_achievements(event_name, event, event.user)
        return json_response(unlocked)

    def validate_hook(headers):
        """
        Validates the hook.
        """
        return True
