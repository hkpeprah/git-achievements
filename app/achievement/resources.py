from tastypie import fields
from django.conf import settings
from django.contrib.auth.models import User
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from app.services.models import Event
from app.achievement.models import Achievement, AchievementCondition, UserProfile, Condition


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
        excludes = ['attributes']
        limit = 20

    def dehydrate(self, bundle):
        # Dehydrate is called to add additional data to the request
        # bundle.
        user = User.objects.get(pk=bundle.data['id'])
        attributes = user.profile.attributes

        bundle.data['avatar'] = attributes['avatar_url']
        bundle.data['username'] = user.username
        bundle.data['rank'] = user.profile.rank
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

    conditions = fields.ListField()

    def dehydrate(self, bundle):
        achievement_id = bundle.data.get('id')
        achievement = Achievement.objects.get(pk=achievement_id)

        achievement_conditions = achievement.conditions.all()
        conditions = []
        for condition in achievement_conditions:
            cr = ConditionResource()
            # Construct bundle for the condition
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

    attributes = fields.DictField(attribute='attributes')
