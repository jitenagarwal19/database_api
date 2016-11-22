from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views
import nse_api.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/', include('hello.urls')),
    url(r'^nse_api/', include('nse_api.urls')),
]
