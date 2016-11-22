from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.perform_database_operations, name='perform_database_operations'),
    url(r'^create_table$', views.create_new_table, name='create_new_table'),
    url(r'^insert/([0-9]{1,20})/$', views.insert_something  , name='insert_something'),
    url(r'^count$', views.get_count_of_temp1 , name='get_count_of_temp1'),
    url(r'content', views.get_content_of_temp1, name='get_content_of_temp1')
]



