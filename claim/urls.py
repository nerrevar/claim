from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'), # index
    path('get_stat', views.stat, name='stat'), # Main statistic
    path('stat_kv', views.stat_kv, name='stat_kv'), # Statistic on kv
    path('stat_question', views.stat_question, name='stat_question'), # Statistic on questions
    path('get_numbers', views.get_numbers, name='get_numbers'),
    path('get_error_fill_data', views.get_error_fill_data, name='get_error_fill_data'), # Data for add_error
    path('write_error', views.write_error, name='write_error'), # For write error xhr
    path('write_error_multiple', views.write_error_multiple, name='write_error_multiple'),
    path('get_groups', views.get_groups, name='get_groups'), # Return group names
    path('get_login', views.get_login, name='get_login'), # Return array of logins
    path('user_add', views.user_add, name='user_add'), # Add user
    path('login', views.login, name='login'), # For login xhr
    path('site_logout', views.site_logout, name='site_logout'), # For logout xhr
]
