from django.conf.urls import patterns, include, url, static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'collabCTF.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'collabCTF.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^settings$', 'collabCTF.views.user_settings', name='settings'),
    url(r'^profile$', 'collabCTF.views.profile', name='profile'),
    url(r'^login$', 'collabCTF.views.log_in', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': "/login"}, name='logout'),
    url(r'^register$', 'collabCTF.views.register', name='register'),
    url(r'^reports$', 'collabCTF.views.reports', name='reports'),
    url(r'^ctf-tools$', 'tools.views.ctf_tools', name='ctf_tools'),
    url(r'^ctf/add$', 'competition.views.add_ctf', name='add_ctf'),
    url(r'^ctf/(?P<ctf_slug>[a-z\d_\-]+)/$', 'competition.views.view_ctf', name='view_ctf'),
    url(r'^ctf/(?P<ctf_slug>[a-z\d_\-]+)/update$', 'competition.views.update_ctf', name='update_ctf'),
    url(r'^ctf/(?P<ctf_slug>[a-z\d_\-]+)/delete$', 'competition.views.delete_ctf', name='delete_ctf'),
    url(r'^ctf/(?P<ctf_slug>[a-z\d_\-]+)/add$', 'competition.views.add_challenge', name='add_challenge'),
    url(r'^ctf/(?P<ctf_slug>[a-z\d_\-]+)/(?P<chall_slug>[a-z\d_\-]+)/$', 'competition.views.view_challenge',
        name='view_challenge'),
    url(r'^ctf/(?P<ctf_slug>[a-z\d_\-]+)/(?P<chall_slug>[a-z\d_\-]+)/update$', 'competition.views.update_challenge',
        name='update_challenge'),
    url(r'^ctf/(?P<ctf_slug>[a-z\d_\-]+)/(?P<chall_slug>[a-z\d_\-]+)/delete$', 'competition.views.delete_challenge',
        name='delete_challenge'),
    url(r'ctf/(?P<ctf_slug>[a-z\d_\-]+)/(?P<chall_slug>[a-z\d_\-]+)/add', 'competition.views.add_file',
        name='add_file'),

    # ajax
    url(r'^ctf/(?P<ctf_slug>[a-z\d_\-]+)/.chart$', 'competition.ajax.chart_data', name='ctf_chart'),
    url(r'^tools/.hash$', 'tools.ajax.hash_val', name='tools_hash'),
    url(r'^tools/.rot$', 'tools.ajax.rot_val', name='tools_rot'),
    url(r'^tools/.base_conversions$', 'tools.ajax.base_conversion_val', name='tools_base_conversion'),
    url(r'^tools/.xor$', 'tools.ajax.xor_val', name='tools_xor'),
    url(r'^tools/.url-quote$', 'tools.ajax.quote_url', name='tools_quote'),
    url(r'^tools/.url-unquote$', 'tools.ajax.unquote_url', name='tools_unquote'),
    url(r'^.challenge-visit$', 'competition.ajax.track_challenge_visit', name='track_challenge_visit'),
)

if settings.DEBUG:
    media_root = settings.MEDIA_ROOT if 'MEDIA_ROOT' in dir(settings) else 'files'
    urlpatterns += static.static(settings.MEDIA_URL, document_root=media_root)
