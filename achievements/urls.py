from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin section urls
    url(r'^admin/', include(admin.site.urls)),

    # Application urls
    url(r'^about/', include('app.shared.urls')),
    url(r'', include('app.achievement.urls')),
)
