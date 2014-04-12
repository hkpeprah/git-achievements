import hashlib


def sha_contains_user_letters(event):
    """
    Returns true if the sha contains all the letters in the
    user's name.
    """
    sha = getattr(event, 'sha', None)
    if not sha:
        return False

    user = event.user.split('')
    sha = sha.split('')
    return len(set(user) & set(sha)) == len(user)


def sha_contains_user(event):
    """
    Returns true if the sha contains the user's name.
    """
    sha = getattr(event, 'sha', None)
    if not sha:
        return False

    return event.user in sha
