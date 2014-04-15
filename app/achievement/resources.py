from tastypie import fields
from django.conf import settings
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from app.services.models import Event
from app.achievement.models import (Achievement, AchievementCondition, UserProfile, Difficulty, UserAchievement,
                                    AchievementType, CustomCondition, ValueCondition, AttributeCondition, Method)


class BaseResource(ModelResource):
    """
    Base ModelResource
    """
    class Meta:
        abstract = True

    def determine_format(self, request):
        formats = settings.TASTYPIE_DEFAULT_FORMATS
        if len(formats) == 1 and formats[0] == 'json':
            return 'application/json'


class UserResource(BaseResource):
    """
    A model resource referring to UserProfile in place of the Django
    Authentication User model.
    """
    class Meta:
        queryset = UserProfile.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'user'
        limit = 20
        max_limit = 20
        excludes = ['approval_votes', 'disapproval_votes', 'attributes']
        filtering = {
            'points': ALL,
            'moderator': ALL,
            'id': ALL,
            'username': ALL
        }

    achievements = fields.ListField()

    def dehydrate(self, bundle):
        # Dehydrate is called to add additional data to the request
        # bundle.
        user = User.objects.get(pk=bundle.data['id'])
        attributes = user.profile.attributes
        # Get the achievements this user has earned
        achievements = []
        for achievement in user.profile.achievements:
            # Construct the achievement bundle resource
            ar = AchievementResource()
            ar_bundle = ar.build_bundle(obj=achievement, request=bundle.request)
            ar_bundle = ar.full_dehydrate(ar_bundle)
            achievements.append(ar_bundle)

        bundle.data['avatar'] = attributes['avatar_url']
        bundle.data['username'] = user.username
        bundle.data['rank'] = user.profile.rank
        bundle.data['achievements'] = achievements
        return bundle


class ConditionResource(BaseResource):
    """
    A model resource that gets the underlying Condition in an
    AchievementCondition ManyRelatedManager.
    """
    class Meta:
        queryset = AchievementCondition.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'condition'
        limit = 20
        max_limit = 20

    def dehydrate(self, bundle):
        """
        Since AchievementCondition is a ManyRelatedManager, determine the
        actual corresponding Condition and populate manually.
        """
        condition_id = bundle.data.get('id')
        condition = AchievementCondition.objects.get(pk=condition_id)

        del bundle.data['object_id']
        condition = condition.condition
        bundle.data['description'] = condition.description
        bundle.data['custom'] = condition.is_custom()
        bundle.data['type'] = condition.condition_type.name
        bundle.data['event'] = condition.event_type.name
        return bundle


class DifficultyResource(BaseResource):
    """
    A model resource for Difficulty model
    """
    class Meta:
        queryset = Difficulty.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'difficulty'
        limit = 20
        max_limit = 20
        filtering = {
            'name': ALL,
            'id': ALL
        }


class AchievementResource(BaseResource):
    """
    A model resource referring to an Achievement.
    """
    class Meta:
        queryset = Achievement.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'achievement'
        limit = 20
        max_limit = 20
        excludes = ['upvoters', 'downvoters']
        filtering = {
            'difficulty': ALL_WITH_RELATIONS,
            'creator': ALL_WITH_RELATIONS,
            'active': ALL
        }

    conditions = fields.ListField()
    difficulty = fields.ToOneField(DifficultyResource, 'difficulty', full=True)
    creator = fields.ToOneField(UserResource, 'creator', full=True, null=True)

    def dehydrate(self, bundle):
        achievement_id = bundle.data.get('id')
        achievement = Achievement.objects.get(pk=achievement_id)

        achievement_conditions = achievement.conditions.all()
        conditions = []
        for condition in achievement_conditions:
            # Construct bundle for the condition
            cr = ConditionResource()
            cr_bundle = cr.build_bundle(obj=condition, request=bundle.request)
            cr_bundle = cr.full_dehydrate(cr_bundle)
            conditions.append(cr_bundle)

        bundle.data['conditions'] = conditions
        bundle.data['count'] = achievement.earned_count
        return bundle


class EventResource(BaseResource):
    """
    A model resource referring to an Event from the services
    api.
    """
    class Meta:
        queryset = Event.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'event'
        excludes = ['payload']
        # This may change, but for now there's only 23 events
        limit = 23
        max_limit = 25

    attributes = fields.DictField(attribute='attributes')


class AchievementTypeResource(BaseResource):
    """
    A model resource for the types of Achievements.
    """
    class Meta:
        queryset = AchievementType.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'achievementtype'
        limit = 20
        max_limit = 20


class CustomConditionResource(BaseResource):
    """
    A model resource for custom conditions.
    """
    class Meta:
        queryset = CustomCondition.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'customcondition'
        limit = 20
        max_limit = 20


class MethodResource(BaseResource):
    """
    A model resource for accessing methods (functions).
    """
    class Meta:
        queryset = Method.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'method'
        excludes = ['callablemethod']
        limit = 20
        max_limit = 20
        filtering = {
            'argument_type': ALL
        }


class ValueConditionResource(BaseResource):
    """
    A model resource for value conditions.
    """
    class Meta:
        queryset = ValueCondition.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'valuecondition'
        limit = 20
        max_limit = 20
        filtering = {
            'method': ALL_WITH_RELATIONS
        }

    method = fields.ToOneField(MethodResource, 'method', full=True)


class AttributeConditionResource(BaseResource):
    """
    A model resource for an attribute conditions.
    """
    class Meta:
        queryset = AttributeCondition.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'attributecondition'
        limit = 20
        max_limit = 20
        filtering = {
            'method': ALL_WITH_RELATIONS
        }

    method = fields.ToOneField(MethodResource, 'method', full=True)


class UserAchievementResource(BaseResource):
    """
    A model resource for accessing achievements users have earned.
    """
    class Meta:
        queryset = UserAchievement.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'userachievement'
        limit = 20
        max_limit = 20
        ordering = ['earned_at']
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'achievement': ALL_WITH_RELATIONS,
            'seen_at': ALL
        }

    user = fields.ToOneField(UserResource, 'user', full=True)
    achievement = fields.ToOneField(AchievementResource, 'achievement', full=True)
