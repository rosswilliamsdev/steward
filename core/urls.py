from django.urls import path
from .views import (
    DashboardView,
    DashboardAPIView,
    TailwindTestView,
    GrantRecommendationListView,
    GrantRecommendationDetailView,
    GrantRecommendationCreateView,
    FundListView,
    FundDetailView,
)

app_name = 'core'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('api/dashboard/', DashboardAPIView.as_view(), name='api-dashboard'),
    path('tailwind-test/', TailwindTestView.as_view(), name='tailwind-test'),

    # Grant recommendation URLs
    path('grants/', GrantRecommendationListView.as_view(), name='grant-list'),
    path('grants/<int:pk>/', GrantRecommendationDetailView.as_view(), name='grant-detail'),
    path('grants/create/', GrantRecommendationCreateView.as_view(), name='grant-create'),

    # Fund URLs
    path('funds/', FundListView.as_view(), name='fund-list'),
    path('funds/<int:pk>/', FundDetailView.as_view(), name='fund-detail'),
]
