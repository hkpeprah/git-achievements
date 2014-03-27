from django.conf.urls import patterns, include, url


urlpatterns = patterns('app.achievement.views',
    # Main application pages.  These pages don't require the
    # user to be authenticated.
    url(r'^/?$', 'index_view', name='index'),
    url(r'^login/?$', 'login_view', name='login'),
    url(r'^logout/?$', 'login_view', name='logout'),
    url(r'^achievements/?$', 'view_achievements', name='view_achievements'),
    url(r'^achievement/view/(?P<achievement_id>\d+)/?$', 'view_achievement', name='view_achievement'),
    url(r'^users/?$', 'view_profiles', name='view_profiles'),
    url(r'^users/(?P<username>\w+)/?$', 'view_profile', name='view_profile'),

    # Information related urls
    url(r'^about/faq/', 'faq', name='faq'),

    # The following urls require the user to be authenticated, as
    # such, they should redirect to the login page if the user isn't authenticated
    url(r'^achievement/create/?$', 'create_achievement', name='create_achievement'),
    url(r'^achievement/vote/?$', 'approve_achievement', {'achievement_id': None}, name='approve_achievement'),
    url(r'^achievement/vote/(?P<achievement_id>\d+)/?$', 'approve_achievement', name='approve_achievement'),
    url(r'^achievement/edit/(?P<achievement_id>\d+)/?$', 'edit_achievement', name='edit_achievement'),
)
