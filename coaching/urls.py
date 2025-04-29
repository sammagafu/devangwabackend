from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'participants', views.ParticipantViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'speakers', views.SpeakerViewSet)
router.register(r'schedules', views.ScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]