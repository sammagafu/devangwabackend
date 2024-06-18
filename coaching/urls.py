from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
# router.register(r'sessions', views.SessionViewSet)
router.register(r'participants', views.ParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
