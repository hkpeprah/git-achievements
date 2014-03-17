from django.conf.urls import patterns, include, url


urlpatterns = patterns('app.achievement.views',
    url(r'^/?$', 'index_view'),
    url(r'^login/?$', 'login_view'),
    url(r'^leaderboard/?$', 'leaderboard_view'),
    # The following urls require the user to be authenticated, as
    # such, they should redirect to the login page if the user isn't authenticated
)
