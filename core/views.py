from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.db.models import Sum
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from .serializers import DashboardSerializer, RecentGrantSerializer
from .models import GrantRecommendation, Fund
from .forms import GrantRecommendationForm


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

        # If donor, get their funds and dashboard data
        if user.is_donor:
            funds = user.funds.all()
            context['funds'] = funds

            # Calculate total balance across all funds
            total_balance = sum(fund.balance for fund in funds)
            context['balance'] = f"{total_balance:,.2f}"

            # Calculate total contributed across all funds
            total_contributed = Decimal('0.00')
            for fund in funds:
                fund_contributions = fund.contributions.aggregate(
                    total=Sum('amount')
                )['total'] or Decimal('0.00')
                total_contributed += fund_contributions
            context['total_contributed'] = f"{total_contributed:,.2f}"

            # Get grants from this year across all funds
            year_start = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            grants_this_year = []
            for fund in funds:
                grants_this_year.extend(
                    fund.grant_recommendations.filter(
                        status='approved',
                        reviewed_at__gte=year_start
                    )
                )

            grants_this_year_total = sum(grant.amount for grant in grants_this_year)
            context['grants_this_year_total'] = f"{grants_this_year_total:,.0f}"
            context['grants_this_year_count'] = len(grants_this_year)

            # Get recent grants (5 most recent across all funds)
            all_grants = []
            for fund in funds:
                all_grants.extend(fund.grant_recommendations.all())

            # Sort by created_at descending and take first 5
            recent_grants = sorted(all_grants, key=lambda g: g.created_at, reverse=True)[:5]
            context['recent_grants'] = recent_grants

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
                    'grants_this_year': {
                        'total': '0.00',
                        'count': 0
                    },
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

            # Calculate grants this year
            year_start = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            grants_this_year = fund.grant_recommendations.filter(
                status='approved',
                reviewed_at__gte=year_start
            )
            grants_this_year_total = grants_this_year.aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0.00')
            grants_this_year_count = grants_this_year.count()

            # Prepare response data
            data = {
                'fund_name': fund.name,
                'balance': str(fund.balance),
                'total_contributed': str(total_contributed),
                'grants_this_year': {
                    'total': str(grants_this_year_total),
                    'count': grants_this_year_count
                },
                'balance_over_time': balance_over_time,
                'recent_grants': RecentGrantSerializer(recent_grants, many=True).data
            }

            # Validate with serializer (but return original data to preserve all fields)
            serializer = DashboardSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            return Response(data)

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


class GrantRecommendationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List all grant recommendations for the current donor.
    Only accessible to donors.
    """
    model = GrantRecommendation
    template_name = 'core/grant_list.html'
    context_object_name = 'grants'

    def test_func(self):
        """Only donors can access this view."""
        return self.request.user.is_donor

    def get_queryset(self):
        """Return grants for current donor's funds, ordered by newest first."""
        return GrantRecommendation.objects.filter(
            fund__donor=self.request.user
        ).select_related('fund').order_by('-created_at')


class GrantRecommendationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Detail view for a single grant recommendation.
    Only accessible to the donor who owns the grant.
    """
    model = GrantRecommendation
    template_name = 'core/grant_detail.html'
    context_object_name = 'grant'

    def test_func(self):
        """Only the grant owner can access this view."""
        grant = self.get_object()
        return self.request.user.is_donor and grant.fund.donor == self.request.user


class GrantRecommendationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Create a new grant recommendation.
    Only accessible to donors.
    """
    model = GrantRecommendation
    form_class = GrantRecommendationForm
    template_name = 'core/grant_form.html'
    success_url = reverse_lazy('core:grant-list')

    def test_func(self):
        """Only donors can access this view."""
        return self.request.user.is_donor

    def get_form_kwargs(self):
        """Pass current user to form for fund filtering."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """Add fund balances as JSON for JavaScript."""
        import json
        context = super().get_context_data(**kwargs)

        # Create fund data dictionary for JavaScript
        funds_data = {}
        for fund in self.request.user.funds.all():
            funds_data[str(fund.id)] = {
                'name': fund.name,
                'balance': float(fund.balance),
            }

        context['funds_data_json'] = json.dumps(funds_data)
        return context

    def form_valid(self, form):
        """Set status to pending on creation."""
        form.instance.status = 'pending'
        messages.success(
            self.request,
            f'Grant recommendation for {form.instance.nonprofit_name} submitted successfully.'
        )
        return super().form_valid(form)


class FundListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List all funds for the current donor.
    Only accessible to donors.
    """
    model = Fund
    template_name = 'core/fund_list.html'
    context_object_name = 'funds'

    def test_func(self):
        """Only donors can access this view."""
        return self.request.user.is_donor

    def get_queryset(self):
        """Return funds for current donor."""
        return self.request.user.funds.all()

    def get_context_data(self, **kwargs):
        """Add total balance and total contributed across all funds."""
        context = super().get_context_data(**kwargs)
        funds = context['funds']

        # Calculate total balance across all funds
        total_balance = sum(fund.balance for fund in funds)
        context['total_balance'] = total_balance

        # Calculate total contributed across all funds
        total_contributed = Decimal('0.00')
        for fund in funds:
            fund_contributions = fund.contributions.aggregate(Sum('amount'))['amount__sum']
            if fund_contributions:
                total_contributed += fund_contributions
        context['total_contributed'] = total_contributed

        return context


class FundDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Detail view for a single fund.
    Only accessible to the donor who owns the fund.
    """
    model = Fund
    template_name = 'core/fund_detail.html'
    context_object_name = 'fund'

    def test_func(self):
        """Only the fund owner can access this view."""
        fund = self.get_object()
        return self.request.user.is_donor and fund.donor == self.request.user

    def get_context_data(self, **kwargs):
        """Add contributions and grants to context."""
        context = super().get_context_data(**kwargs)
        context['contributions'] = self.object.contributions.order_by('-date')
        context['grants'] = self.object.grant_recommendations.order_by('-created_at')
        return context
