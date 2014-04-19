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
                url=reverse('view_achievement', achievement_id=instance.pk))

    return None


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

    notify.send(instance, recipient=instance.user.user, verb='was unlocked',
        description='You have unlocked "{0}"'.format(instance.achievement.name),
        url=reverse('view_achievement', achievement_id=instance.pk))

    return None
