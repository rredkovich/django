
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.gis import admin
from django.conf import settings

import api.views as views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'restaurant.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.closest),
    url(r'^restaurants/(?P<rest_pk>[A-Z0-9]+)/comment/$', views.comment),
    url(r'', include('social.apps.django_app.urls', namespace='social')),

    # url(r'^logout/$', views.log_out),
)

