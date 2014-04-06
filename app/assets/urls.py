from tastypie.api import Api
from django.conf.urls import patterns, include, url

from app.assets.resources import UserResource


# Configure the API
api = Api(api_name='v1')
api.register(UserResource())


# Regular url patterns
urlpatterns = patterns('',
    url(r'^api/', include(api.urls)),
)
