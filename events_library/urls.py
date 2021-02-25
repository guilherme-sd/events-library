from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events_library.application.views import EventViewSet

EVENT_ROUTER = DefaultRouter()
EVENT_ROUTER.register(r'event', EventViewSet, basename='event')

urlpatterns = [
    path('', include(EVENT_ROUTER.urls))
]
