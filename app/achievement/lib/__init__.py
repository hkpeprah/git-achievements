from sha import contains_user_sha


def callable(function):
    return hasattr(function, '__call__')
