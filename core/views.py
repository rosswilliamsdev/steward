from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from .serializers import DashboardSerializer, RecentGrantSerializer


class TailwindTestView(TemplateView):
    """Test page to verify Tailwind CSS configuration."""
    template_name = 'core/tailwind_test.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard - shows different content based on user role.
    """
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Add role-specific context
        context['is_donor'] = user.is_donor
        context['is_admin'] = user.is_admin

        # If donor, get their funds
        if user.is_donor:
            context['funds'] = user.funds.all()

        return context


class DashboardAPIView(APIView):
    """
    API endpoint for donor dashboard data.
    Returns fund balance, contribution total, balance over time, and recent grants.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET /api/dashboard/
        Returns dashboard data for the authenticated donor.
        """
        try:
            # Only donors can access this endpoint
            if not request.user.is_donor:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Get the donor's first fund (sorted by -created_at)
            fund = request.user.funds.first()

            if not fund:
                # No fund exists - return empty but valid structure
                return Response({
                    'fund_name': '',
                    'balance': '0.00',
                    'total_contributed': '0.00',
                    'balance_over_time': [],
                    'recent_grants': []
                })

            # Calculate total contributed
            total_contributed = fund.contributions.aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0.00')

            # Get recent grants (5 most recent)
            recent_grants = fund.grant_recommendations.all()[:5]

            # Calculate balance over time (last 12 months)
            balance_over_time = self._calculate_balance_over_time(fund)

            # Prepare response data
            data = {
                'fund_name': fund.name,
                'balance': str(fund.balance),
                'total_contributed': str(total_contributed),
                'balance_over_time': balance_over_time,
                'recent_grants': RecentGrantSerializer(recent_grants, many=True).data
            }

            # Validate with serializer
            serializer = DashboardSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data)

        except Exception:
            # On any error, return HTTP 500 with empty body
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _calculate_balance_over_time(self, fund):
        """
        Calculate monthly balance snapshots for the last 12 months.
        Returns list of {month: 'YYYY-MM', balance: 'XXX.XX'} dicts.
        """
        balance_data = []
        today = timezone.now().date()

        # Start from 12 months ago
        start_month = (today - relativedelta(months=11)).replace(day=1)

        # Initialize running balance at zero
        running_balance = Decimal('0.00')

        # Get all contributions and approved grants for this fund
        contributions = fund.contributions.all().order_by('date')
        approved_grants = fund.grant_recommendations.filter(
            status='approved'
        ).order_by('created_at')

        # Process each of the last 12 months
        for i in range(12):
            month_start = start_month + relativedelta(months=i)
            month_end = month_start + relativedelta(months=1) - timedelta(days=1)

            # Convert to timezone-aware datetime for comparison with DateTimeField
            month_start_dt = timezone.make_aware(
                datetime.combine(month_start, datetime.min.time())
            )
            month_end_dt = timezone.make_aware(
                datetime.combine(month_end, datetime.max.time())
            )

            # Add contributions in this month
            month_contributions = contributions.filter(
                date__gte=month_start,
                date__lte=month_end
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            # Subtract approved grants in this month (reviewed_at is DateTimeField)
            month_grants = approved_grants.filter(
                reviewed_at__gte=month_start_dt,
                reviewed_at__lte=month_end_dt
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            # Update running balance
            running_balance += month_contributions - month_grants

            # Append snapshot
            balance_data.append({
                'month': month_start.strftime('%Y-%m'),
                'balance': str(running_balance)
            })

        return balance_data
