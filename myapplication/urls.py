from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.view_form, name='view_form'),
    # url(r'^create_form$', views.create_form, name='create_form'),
    # url(r'^created_form$', views.created_form, name='created_form'),
]
