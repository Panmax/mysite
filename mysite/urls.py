from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'school.views.index'),
    url(r'^index/$', 'school.views.index'),
    url(r'^login/$', 'school.views.index'),
    url(r'^logout/$', 'school.views.logout'),
    url(r'^regist/$', 'school.views.registPage'),
    url(r'^comming/$', 'school.views.comming'),
    url(r'^publish/$', 'school.views.publish'),
    url(r'^publish/success/$', 'school.views.success'),
    url(r'^receive/$', 'school.views.receive'),
    url(r'^receive/(?P<offset>\d{1,2})/$','school.views.receive'),
    url(r'^help/$', 'school.views.help'),
    url(r'^task/$', 'school.views.task'),
    url(r'^select/(?P<id>\d+)/$','school.views.select'),
    url(r'^delete/(?P<id>\d+)/$','school.views.delete'),
    # url(r'^regist/$', 'school.views.regist'),
    # url(r'^login/$', 'school.views.login'),
    # url(r'^index/$', 'school.views.index'),
    # url(r'^logout/$', 'school.views.logout'),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/jiapan/mysite/static'}),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
