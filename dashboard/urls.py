from django.urls import path
from .views import DashboardStatsView, EarningsChartView, TopInstructorsView, CommunityStatsView, EventStatsView, TrafficSourcesView

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('payments/earnings/chart/', EarningsChartView.as_view(), name='earnings-chart'),
    path('top-instructors/', TopInstructorsView.as_view(), name='top-instructors'),
    path('community-stats/', CommunityStatsView.as_view(), name='community-stats'),
    path('event-stats/', EventStatsView.as_view(), name='event-stats'),
    path('traffic-sources/', TrafficSourcesView.as_view(), name='traffic-sources'),
]