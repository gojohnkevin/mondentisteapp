from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'login/$', 'login', name='login'),
)

urlpatterns += patterns('',
    url(r'logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)
