from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home_page$', views.home_page, name='home_page'),
    # url(r'^sign_up$', views.sign_up, name='sign_up'),
    url(r'^sign_in$', views.sign_in, name='sign_in'),
    url(r'^sign_user_up$', views.sign_user_up, name='sign_user_up'),
    url(r'^sign_user_in$', views.sign_user_in, name='sign_user_in'),
    url(r'^member_home_page$', views.member_home_page, name='member_home_page'),
    url(r'^failed_login$', views.failed_login, name='failed_login'),
    url(r'^create_report$', views.create_report, name='create_report'),
    url(r'^view_reports$', views.view_reports, name='view_reports'),
    url(r'^view_reports_folder', views.view_reports_folder, name="view_reports_folder"),
    url(r'^manage_reports$', views.manage_reports, name="manage_reports"),
    url(r'^delete_report$', views.delete_report, name="delete_report"),
    url(r'^add_files$', views.add_files, name="add_files"),
    url(r'^remove_files$', views.remove_files, name="remove_files"),
    url(r'^create_folder$', views.create_folder, name="create_folder"),
    url(r'^add_reports_folder$', views.add_reports_folder, name="add_reports_folder"),
    url(r'^remove_report_folder$', views.remove_report_folder, name="remove_report_folder"),
    url(r'^rename_folder$', views.rename_folder, name="rename_folder"),
    url(r'^delete_folder$', views.delete_folder, name="delete_folder"),
    url(r'^download_unencrypted_files$', views.download_unencrypted_files, name="download_unencrypted_files"),
    url(r'^search_reports$', views.search_reports, name="search_reports"),
]
