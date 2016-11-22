from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^read_shit$', views.read_me_the_shit, name='read_me_the_shit'),
    url(r'^is_index_present/([a-z0-9]{1,20})/$', views.is_index_present, name='is_index_present'),
    url(r'^get_content_indices$', views.get_contents_indices, name='get_contents_indices'),
    url(r'^read_data_from_local$', views.read_data_from_local, name='read_data_from_local'),
    url(r'^save_data_from_local$', views.save_data_from_local, name='save_data_from_local'),
    url(r'^nse_ind/([a-z0-9]{1,20})/start-date/([0-9]{4}-[0-9]{2}-[0-9]{2})/end-date/([0-9]{4}-[0-9]{2}-[0-9]{2})/$', views.is_present, name='is_present'),
]



