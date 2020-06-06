from django.urls import path

from . import views

urlpatterns = [
    path('add_error', views.add_error, name='add_error'),
    path('', views.stat, name='stat'),
    path('write_error', views.write_error, name='write_error'),
    path('stat_kv', views.stat_kv, name='stat_kv'),
    path('stat_question', views.stat_question, name='stat_question')
]
