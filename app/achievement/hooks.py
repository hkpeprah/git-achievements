from django.contrib.auth.models import User

from app.achievement.models import UserProfile, Achievement


def check_for_unlocked_achievements(event, payload, user):
    """
    Checks if a user has unlocked any achievements, given the event
    and event payload as input.

    @param event: Name of the event
    @param payload: Dictionary of key-value event data
    @param user: The User/UserProfile model or name of a user
    @return: listof Achievement
    """
    if isinstance(user, basestring):
        # There's a guarantee that usernames are unique
        if User.objects.filter(username=user).count() == 1:
            user = User.objects.get(username=user).profile
        elif UserProfile.objects.filter(user__username=user).count() == 1:
            user = UserProfile.objects.get(user__username=user)
        else:
            return []
    elif isinstance(user, User):
        user = user.profile
    else:
        raise ValueError("Expected a string, User or UserProfile object, found %s" % type(user))

    achievements = Achievement.objects.exclude(pk__in=
        map(lambda u: u.pk, user.achievements.all()))
    unlocked_achievements = []

    for achievement in achievements:
        if achievement.unlocked(event, payload):
            user.achievements.add(achievement)
            user.points = user.points + achievement.points
            unlocked_achievements.append(achievement.to_json())

    user.save()
    return unlocked_achievements
