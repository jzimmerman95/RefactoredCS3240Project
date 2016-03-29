from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.sign_up, name='sign_up'),
    url(r'^sign_user_in$', views.sign_user_in, name='sign_user_in'),
    url(r'^successful_signup$', views.successful_signup, name='successful_signup'),
    # url(r'^created_form$', views.created_form, name='created_form'),
]
