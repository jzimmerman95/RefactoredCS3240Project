from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.sign_up, name='sign_up'),
    # url(r'^create_form$', views.create_form, name='create_form'),
    # url(r'^created_form$', views.created_form, name='created_form'),
]
