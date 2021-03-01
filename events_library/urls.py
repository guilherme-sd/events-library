from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .application import EventViewSet

EVENT_ROUTER = DefaultRouter()
EVENT_ROUTER.register('', EventViewSet, basename='event')

urlpatterns = [
    path('', include(EVENT_ROUTER.urls)),
]
