from django.db.models import Q
from django.contrib.auth.models import User

from app.achievement.models import UserProfile, Achievement, UserAchievement


def check_for_unlocked_achievements(event, payload, user=None):
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

    unlocked_achievements = []
    if user:
        achievements = Achievement.objects.exclude(Q(active=False) | Q(pk__in=
            map(lambda u: u.pk, user.achievements)))
    else:
        achievements = Achievement.objects.exclude(active=False)

    for achievement in achievements:
        if achievement.unlocked(event, payload):
            unlocked_achievements.append(achievement.to_json())
            if user:
                unlocked_achievement = UserAchievement(achievement=achievement, user=user)
                unlocked_achievement.save()
                user.points = user.points + achievement.points

    if user:
        user.save()

    return unlocked_achievements
