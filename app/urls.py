from django.contrib import admin
from django.urls import re_path,include
from app import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^login$', views.login, name='login'),
    re_path(r'^RTO$', views.RTO, name='RTO'),
    re_path(r'^user$', views.user, name='user'),
    re_path(r'^agent$', views.agent, name='agent'),
    re_path(r'^logout$', views.logout, name='logout'),
    re_path(r'^agentVehicleAddForm$', views.agentVehicleAddForm, name='agentVehicleAddForm'),
    re_path(r'^listPageAgent$', views.listPageAgent, name='listPageAgent'),
    re_path(r'^agentVehicleEditForm/(?P<id>\d+)$', views.agentVehicleEditForm, name='agentVehicleEditForm'),
    re_path(r'^agentVehicleEditFormSubmit/(?P<id>\d+)$', views.agentVehicleEditFormSubmit, name='agentVehicleEditFormSubmit'),
    re_path(r'^RTOVehicleRegNoAddForm/(?P<id>\d+)$', views.RTOVehicleRegNoAddForm, name='RTOVehicleRegNoAddForm'),
]
