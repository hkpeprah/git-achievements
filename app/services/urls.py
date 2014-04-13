from django.conf.urls import patterns, include, url


urlpatterns = patterns('app.services.views',
    url(r'^hooks/web', 'web_hook', name='web_hook'),
    url(r'^hooks/local', 'web_local_hook', name='web_local_hook'),
    url(r'^events/(?P<service>\w+)/?$', 'service_events', name='service_events'),
)
