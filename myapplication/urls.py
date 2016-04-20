from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home_page$', views.home_page, name='home_page'),
    url(r'^sign_up$', views.sign_up, name='sign_up'),
    url(r'^sign_in$', views.sign_in, name='sign_in'),
    url(r'^sign_user_up$', views.sign_user_up, name='sign_user_up'),
    url(r'^sign_user_in$', views.sign_user_in, name='sign_user_in'),
    url(r'^member_home_page$', views.member_home_page, name='member_home_page'),
    url(r'^failed_login$', views.failed_login, name='failed_login'),
    url(r'^create_group$', views.create_group, name='create_group'),
    url(r'^create_user_group$', views.create_user_group, name='create_user_group'),
]
