from rest_framework import serializers
from .models import GrantRecommendation


class RecentGrantSerializer(serializers.ModelSerializer):
    """Serializer for recent grants in dashboard API."""

    class Meta:
        model = GrantRecommendation
        fields = ['id', 'nonprofit_name', 'amount', 'status', 'created_at']


class BalanceOverTimeSerializer(serializers.Serializer):
    """Serializer for monthly balance snapshots."""
    month = serializers.CharField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)


class DashboardSerializer(serializers.Serializer):
    """Serializer for donor dashboard data."""
    fund_name = serializers.CharField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_contributed = serializers.DecimalField(max_digits=10, decimal_places=2)
    balance_over_time = BalanceOverTimeSerializer(many=True)
    recent_grants = RecentGrantSerializer(many=True)
