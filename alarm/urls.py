from django.urls import path
from .views import AlarmListCreateView, AlarmDetailView, AlarmToggleView

urlpatterns = [
    path('api/alarms/', AlarmListCreateView.as_view(), name='alarm-list-create'),
    path('api/alarms/<int:pk>/', AlarmDetailView.as_view(), name='alarm-detail'),
    path('api/alarms/<int:pk>/toggle/', AlarmToggleView.as_view(), name='alarm-toggle'),
]