from django.urls import path
from .views import (
    DashboardView,
    DashboardAPIView,
    TailwindTestView,
    GrantRecommendationCreateView,
)

app_name = 'core'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('api/dashboard/', DashboardAPIView.as_view(), name='api-dashboard'),
    path('tailwind-test/', TailwindTestView.as_view(), name='tailwind-test'),

    # Grant recommendation URLs
    path('grants/create/', GrantRecommendationCreateView.as_view(), name='grant-create'),
    # Placeholder for grant-list - will be implemented in Phase 4
    # path('grants/', GrantRecommendationListView.as_view(), name='grant-list'),
]
