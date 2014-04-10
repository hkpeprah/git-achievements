from django.contrib import admin
from django.conf.urls import patterns, include, url


# Enables the admin application
admin.autodiscover()


"""
Add urls here for the main application paths.  Empty string paths will
cause Django to check all the paths within that application.
"""
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^services/', include('app.services.urls'), name='services'),
    url(r'', include('social.apps.django_app.urls', namespace='social'), name='social'),
    # If all else fails, delegate to the achievements application
    # as that is most likely where the url is pointing.
    url(r'', include('app.achievement.urls', app_name='achievements')),
)
