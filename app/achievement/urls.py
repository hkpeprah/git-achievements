from django.conf.urls import patterns, include, url


urlpatterns = patterns('app.achievement.views',
    # Main application pages.  These pages don't require the
    # user to be authenticated.
    url(r'^/?$', 'index_view'),
    url(r'^login/?$', 'login_view'),
    url(r'^logout/?$', 'login_view'),
    url(r'^leaderboard/?$', 'leaderboard_view'),


    # The following urls require the user to be authenticated, as
    # such, they should redirect to the login page if the user isn't authenticated

    # Achievement model urls
    url(r'^achievement/create/?$', 'create_achievement'),
    url(r'^achievement/vote/(?P<achievement_id>\d+)/?$', 'approve_achievement'),
    url(r'^achievement/edit/(?P<achievement_id>\d+)/?$', 'edit_achievement'),
    url(r'^achievement/view/(?P<achievement_id>\d+)/?$', 'view_achievement'),

    # User Profiles
    url(r'^users/(?P<user_id>\d+)/?$', 'view_profile'),
)
