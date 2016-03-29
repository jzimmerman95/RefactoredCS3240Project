from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^sign_up$', views.sign_up, name='sign_up'),
    url(r'^sign_in$', views.sign_in, name='sign_in'),
    url(r'^sign_user_up$', views.sign_user_up, name='sign_user_up'),
    url(r'^successful_signup$', views.successful_signup, name='successful_signup'),
]
