from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')
router.register(r'participants', views.ParticipantViewSet, basename='participant')
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'speakers', views.SpeakerViewSet, basename='speaker')
router.register(r'schedules', views.ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', include(router.urls)),
]