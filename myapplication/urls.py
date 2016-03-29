from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.sign_up, name='sign_up'),
    url(r'^sign_user_in$', views.sign_user_in, name='sign_user_in'),
    url(r'^signup_failed$', views.signup_failed, name='signup_failed'),
    # url(r'^created_form$', views.created_form, name='created_form'),
]
