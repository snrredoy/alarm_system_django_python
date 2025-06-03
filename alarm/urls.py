from django.urls import path
from . import views

urlpatterns = [
    path('', views.alarm_view, name='alarm'),
]