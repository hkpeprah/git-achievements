from tastypie import fields
from django.contrib.auth.models import User
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from app.achievement.models import Achievement, AchievementCondition, UserProfile


class UserResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'user'
        excludes = ['attributes']
        filtering = {
            'slug': ALL
        }

    def dehydrate(self, bundle):
        # Dehydrate is called to add additional data to the request
        # bundle.
        user = User.objects.get(pk=bundle.data['id'])
        attributes = user.profile.attributes

        bundle.data['avatar'] = attributes['avatar_url']
        bundle.data['username'] = user.username
        bundle.data['rank'] = user.profile.rank
        return bundle
