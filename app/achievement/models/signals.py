from notifications import notify
from django.db.models.signals import post_save

from app.achievement.utils import reverse_with_query_params as reverse


def notify_achievement_approved(sender, instance, created, **kwargs):
    """
    Notifies a user that an achievement they've created has been approved.

    @param sender: The model class
    @param instance: Instance of the model class being saved
    @param created: True if this is newly created.
    @param kwargs: Dictionary of key-value arguments.
    @return: None
    """
    if not created and instance.active:
        creator = instance.creator
        if creator:
            # Only notify if there's actually a creator attached to the achievement
            notify.send(instance, recipient=creator.user, verb='was approved.',
                description='Your achievement, {0} was approved.'.format(instance.name),
                url=reverse('view_achievement', achievement_id=instance.achievement.pk))


def notify_achievement_unlocked(sender, instance, created, **kwargs):
    """
    Notifies a user that they have unlocked an achievement.

    @param sender: The model class
    @param instance: Instance of the model class being saved
    @param created: True if this is newly created.
    @param kwargs: Dictionary of key-value arguments.
    @return: None
    """
    if not created:
        return None

    if instance.achievement.badge:
        instance.user.badges.add(instance.achievement.badge)
    instance.user.points += instance.achievement.points
    instance.user.save()

    notify.send(instance, recipient=instance.user.user, verb='was unlocked',
        description='You have unlocked "{0}"'.format(instance.achievement.name),
        url=reverse('view_achievement', achievement_id=instance.achievement.pk))


def on_achievement_deleted(sender, instance, *args, **kwargs):
    """
    Achievements have a OneToOne relation with a badge, which we now need to
    cleanup.

    @param sender: The model that triggers the signal
    @param instance: Instance of the sender
    @param args: list of arguments
    @param kwargs: Dictionary of key-value arguments
    """
    if instance.badge:
        instance.badge.delete()


def before_userachievement_deleted(sender, instance, **kwargs):
    """
    When deleting a user achievement, decrement the user's points to reflect the
    change.

    @param sender: The model that triggers the signal
    @param instance: Instance of the sender
    @param kwargs: Dictionary of key-value arguments
    """
    points = instance.achievement.points
    user = instance.user
    user.points = max(user.points - points, 0)
    user.save()
