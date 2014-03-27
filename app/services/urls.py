from django.conf.urls import patterns, include, url


urlpatterns = patterns('app.services.views',
    url(r'^events/(?P<service>\w+)/?$', 'service_events', name='service_events'),
)
