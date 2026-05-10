from django.urls import path
from .views import DashboardView, DashboardAPIView, TailwindTestView

app_name = 'core'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('api/dashboard/', DashboardAPIView.as_view(), name='api-dashboard'),
    path('tailwind-test/', TailwindTestView.as_view(), name='tailwind-test'),
]
