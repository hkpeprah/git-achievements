from django.conf.urls import patterns, include, url


urlpatterns = patterns('app.shared.views',
    # Help pages for assets
    # Generic about page
    url(r'^$', 'help_view'),
    # These pages describe what the models are and list them for the users
    url(r'^users/?$', 'view_users'),
    url(r'^badges/?', 'view_badges'),
    url(r'^achievements/?', 'view_achievements'),
)
