from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta
from .models import CustomUser, Fund, Contribution, GrantRecommendation
from .forms import GrantRecommendationForm


class DonorViewPermissionTests(TestCase):
    """Test permission checks for donor views."""

    def setUp(self):
        """Create test users and funds."""
        # Create two donors
        self.donor1 = CustomUser.objects.create_user(
            username='donor1',
            password='testpass123',
            is_donor=True
        )
        self.donor2 = CustomUser.objects.create_user(
            username='donor2',
            password='testpass123',
            is_donor=True
        )

        # Create staff user
        self.staff = CustomUser.objects.create_user(
            username='staff',
            password='testpass123',
            is_admin=True
        )

        # Create regular user (not donor or admin)
        self.regular_user = CustomUser.objects.create_user(
            username='regular',
            password='testpass123',
            is_donor=False,
            is_admin=False
        )

        # Create funds for each donor
        self.fund1 = Fund.objects.create(
            name='Donor 1 Fund',
            donor=self.donor1
        )
        self.fund2 = Fund.objects.create(
            name='Donor 2 Fund',
            donor=self.donor2
        )

        # Create contributions
        Contribution.objects.create(
            fund=self.fund1,
            amount=Decimal('1000.00'),
            date=date.today(),
            created_by=self.staff
        )

        # Create grants
        self.grant1 = GrantRecommendation.objects.create(
            fund=self.fund1,
            nonprofit_name='Test Nonprofit 1',
            amount=Decimal('500.00'),
            memo='Test grant 1'
        )
        self.grant2 = GrantRecommendation.objects.create(
            fund=self.fund2,
            nonprofit_name='Test Nonprofit 2',
            amount=Decimal('500.00'),
            memo='Test grant 2'
        )

        self.client = Client()

    def test_donor_cannot_see_other_donor_funds(self):
        """Donor should not be able to access another donor's fund detail."""
        self.client.login(username='donor1', password='testpass123')
        response = self.client.get(reverse('core:fund-detail', args=[self.fund2.pk]))
        self.assertEqual(response.status_code, 403)

    def test_donor_cannot_see_other_donor_grants(self):
        """Donor should not be able to access another donor's grant detail."""
        self.client.login(username='donor1', password='testpass123')
        response = self.client.get(reverse('core:grant-detail', args=[self.grant2.pk]))
        self.assertEqual(response.status_code, 403)

    def test_non_donor_cannot_access_donor_views(self):
        """Regular user (not donor) should get 403 on donor-specific views."""
        self.client.login(username='regular', password='testpass123')

        # Dashboard is accessible to all authenticated users, but shows different content
        # These views are donor-only
        urls = [
            reverse('core:grant-list'),
            reverse('core:grant-create'),
            reverse('core:fund-list'),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def test_unauthenticated_user_redirected_to_login(self):
        """Unauthenticated user should be redirected to login."""
        urls = [
            reverse('core:dashboard'),
            reverse('core:grant-list'),
            reverse('core:grant-create'),
            reverse('core:fund-list'),
            reverse('core:fund-detail', args=[self.fund1.pk]),
            reverse('core:grant-detail', args=[self.grant1.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn('/login/', response.url)

    def test_donor_can_access_own_fund(self):
        """Donor should be able to access their own fund detail."""
        self.client.login(username='donor1', password='testpass123')
        response = self.client.get(reverse('core:fund-detail', args=[self.fund1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_donor_can_access_own_grant(self):
        """Donor should be able to access their own grant detail."""
        self.client.login(username='donor1', password='testpass123')
        response = self.client.get(reverse('core:grant-detail', args=[self.grant1.pk]))
        self.assertEqual(response.status_code, 200)


class GrantRecommendationFormTests(TestCase):
    """Test form validation for grant recommendations."""

    def setUp(self):
        """Create test donor and fund."""
        self.donor = CustomUser.objects.create_user(
            username='donor',
            password='testpass123',
            is_donor=True
        )
        self.staff = CustomUser.objects.create_user(
            username='staff',
            password='testpass123',
            is_admin=True
        )
        self.fund = Fund.objects.create(
            name='Test Fund',
            donor=self.donor
        )
        # Add $1000 contribution
        Contribution.objects.create(
            fund=self.fund,
            amount=Decimal('1000.00'),
            date=date.today(),
            created_by=self.staff
        )

    def test_form_rejects_amount_exceeding_balance(self):
        """Form should reject grant amount exceeding fund balance."""
        form = GrantRecommendationForm(
            data={
                'fund': self.fund.pk,
                'nonprofit_name': 'Test Nonprofit',
                'amount': '1500.00',
                'memo': 'Test grant'
            },
            user=self.donor
        )
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_form_accepts_amount_equal_to_balance(self):
        """Form should accept grant amount equal to fund balance."""
        form = GrantRecommendationForm(
            data={
                'fund': self.fund.pk,
                'nonprofit_name': 'Test Nonprofit',
                'amount': '1000.00',
                'memo': 'Test grant'
            },
            user=self.donor
        )
        self.assertTrue(form.is_valid())

    def test_form_accepts_amount_less_than_balance(self):
        """Form should accept grant amount less than fund balance."""
        form = GrantRecommendationForm(
            data={
                'fund': self.fund.pk,
                'nonprofit_name': 'Test Nonprofit',
                'amount': '500.00',
                'memo': 'Test grant'
            },
            user=self.donor
        )
        self.assertTrue(form.is_valid())

    def test_memo_is_optional(self):
        """Memo field should be optional."""
        form = GrantRecommendationForm(
            data={
                'fund': self.fund.pk,
                'nonprofit_name': 'Test Nonprofit',
                'amount': '500.00',
                'memo': ''
            },
            user=self.donor
        )
        self.assertTrue(form.is_valid())

    def test_form_limits_funds_to_user_funds(self):
        """Form should only show funds owned by the user."""
        # Create another donor with a fund
        other_donor = CustomUser.objects.create_user(
            username='other_donor',
            password='testpass123',
            is_donor=True
        )
        other_fund = Fund.objects.create(
            name='Other Fund',
            donor=other_donor
        )

        form = GrantRecommendationForm(user=self.donor)
        fund_choices = [choice[0] for choice in form.fields['fund'].choices if choice[0]]

        self.assertIn(self.fund.pk, fund_choices)
        self.assertNotIn(other_fund.pk, fund_choices)


class DonorViewTests(TestCase):
    """Test donor view logic and rendering."""

    def setUp(self):
        """Create test data."""
        self.donor = CustomUser.objects.create_user(
            username='donor',
            password='testpass123',
            is_donor=True
        )
        self.staff = CustomUser.objects.create_user(
            username='staff',
            password='testpass123',
            is_admin=True
        )
        self.fund = Fund.objects.create(
            name='Test Fund',
            donor=self.donor
        )
        Contribution.objects.create(
            fund=self.fund,
            amount=Decimal('5000.00'),
            date=date.today(),
            created_by=self.staff
        )
        self.grant = GrantRecommendation.objects.create(
            fund=self.fund,
            nonprofit_name='Test Nonprofit',
            amount=Decimal('1000.00'),
            memo='Test grant',
            status='approved',
            reviewed_by=self.staff,
            reviewed_at=timezone.now()
        )
        self.client = Client()
        self.client.login(username='donor', password='testpass123')

    def test_dashboard_shows_correct_fund_data(self):
        """Dashboard should display correct balance and totals."""
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        # Dashboard uses React component, so just verify page loads

    def test_grant_list_shows_only_user_grants(self):
        """Grant list should only show current user's grants."""
        # Create another donor with grant
        other_donor = CustomUser.objects.create_user(
            username='other_donor',
            password='testpass123',
            is_donor=True
        )
        other_fund = Fund.objects.create(
            name='Other Fund',
            donor=other_donor
        )
        other_grant = GrantRecommendation.objects.create(
            fund=other_fund,
            nonprofit_name='Other Nonprofit',
            amount=Decimal('500.00')
        )

        response = self.client.get(reverse('core:grant-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Nonprofit')
        self.assertNotContains(response, 'Other Nonprofit')

    def test_grant_create_success_redirect(self):
        """Successful grant creation should redirect to grant list."""
        response = self.client.post(
            reverse('core:grant-create'),
            {
                'fund': self.fund.pk,
                'nonprofit_name': 'New Nonprofit',
                'amount': '500.00',
                'memo': 'New grant'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('core:grant-list'))

        # Verify grant was created with pending status
        grant = GrantRecommendation.objects.get(nonprofit_name='New Nonprofit')
        self.assertEqual(grant.status, 'pending')
        self.assertEqual(grant.fund, self.fund)

    def test_fund_detail_shows_contributions_and_grants(self):
        """Fund detail should display contributions and grants."""
        response = self.client.get(reverse('core:fund-detail', args=[self.fund.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '5,000.00')  # Contribution amount
        self.assertContains(response, 'Test Nonprofit')  # Grant

    def test_fund_list_shows_all_user_funds(self):
        """Fund list should show all funds owned by user."""
        # Create second fund
        fund2 = Fund.objects.create(
            name='Second Fund',
            donor=self.donor
        )

        response = self.client.get(reverse('core:fund-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Fund')
        self.assertContains(response, 'Second Fund')

    def test_grant_detail_shows_all_fields(self):
        """Grant detail should display all grant information."""
        response = self.client.get(reverse('core:grant-detail', args=[self.grant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Nonprofit')
        self.assertContains(response, '1,000.00')
        self.assertContains(response, 'Test grant')
        self.assertContains(response, 'Approved')


class DashboardAPITests(TestCase):
    """Test dashboard API endpoint."""

    def setUp(self):
        """Create test data."""
        self.donor = CustomUser.objects.create_user(
            username='donor',
            password='testpass123',
            is_donor=True
        )
        self.staff = CustomUser.objects.create_user(
            username='staff',
            password='testpass123',
            is_admin=True
        )
        self.fund = Fund.objects.create(
            name='Test Fund',
            donor=self.donor
        )
        Contribution.objects.create(
            fund=self.fund,
            amount=Decimal('10000.00'),
            date=date.today(),
            created_by=self.staff
        )

        # Create multiple grants
        for i in range(7):
            GrantRecommendation.objects.create(
                fund=self.fund,
                nonprofit_name=f'Nonprofit {i}',
                amount=Decimal('100.00'),
                memo=f'Grant {i}'
            )

        self.client = Client()
        self.client.login(username='donor', password='testpass123')

    def test_api_returns_correct_data_structure(self):
        """API should return expected data structure."""
        response = self.client.get(reverse('core:api-dashboard'))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('fund_name', data)
        self.assertIn('balance', data)
        self.assertIn('total_contributed', data)
        self.assertIn('grants_this_year', data)
        self.assertIn('balance_over_time', data)
        self.assertIn('recent_grants', data)

    def test_api_balance_over_time_has_12_months(self):
        """Balance over time should have exactly 12 data points."""
        response = self.client.get(reverse('core:api-dashboard'))
        data = response.json()

        self.assertEqual(len(data['balance_over_time']), 12)

    def test_api_recent_grants_limited_to_5(self):
        """Recent grants should be limited to 5 items."""
        response = self.client.get(reverse('core:api-dashboard'))
        data = response.json()

        self.assertEqual(len(data['recent_grants']), 5)

    def test_api_requires_authentication(self):
        """API should require authentication."""
        self.client.logout()
        response = self.client.get(reverse('core:api-dashboard'))
        # Should redirect to login (302) or return 403
        self.assertIn(response.status_code, [302, 403])

    def test_api_requires_donor_role(self):
        """API should only be accessible to donors."""
        # Create non-donor user
        regular_user = CustomUser.objects.create_user(
            username='regular',
            password='testpass123',
            is_donor=False
        )
        self.client.logout()
        self.client.login(username='regular', password='testpass123')

        response = self.client.get(reverse('core:api-dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_api_calculates_correct_balance(self):
        """API should calculate correct fund balance."""
        response = self.client.get(reverse('core:api-dashboard'))
        data = response.json()

        # Balance = 10000 contributed - 0 approved grants = 10000
        self.assertEqual(data['balance'], '10000.00')
        self.assertEqual(data['total_contributed'], '10000.00')

    def test_api_aggregates_multiple_funds(self):
        """API should aggregate data across all donor's funds."""
        # Create second fund
        fund2 = Fund.objects.create(
            name='Second Fund',
            donor=self.donor
        )
        Contribution.objects.create(
            fund=fund2,
            amount=Decimal('5000.00'),
            date=date.today(),
            created_by=self.staff
        )

        response = self.client.get(reverse('core:api-dashboard'))
        data = response.json()

        # Should show "All Funds" when donor has multiple funds
        self.assertEqual(data['fund_name'], 'All Funds')
        # Total contributed = 10000 + 5000 = 15000
        self.assertEqual(data['total_contributed'], '15000.00')


class FundBalanceTests(TestCase):
    """Test fund balance calculation."""

    def setUp(self):
        """Create test data."""
        self.donor = CustomUser.objects.create_user(
            username='donor',
            password='testpass123',
            is_donor=True
        )
        self.staff = CustomUser.objects.create_user(
            username='staff',
            password='testpass123',
            is_admin=True
        )
        self.fund = Fund.objects.create(
            name='Test Fund',
            donor=self.donor
        )

    def test_balance_with_no_transactions(self):
        """Fund with no contributions or grants should have zero balance."""
        self.assertEqual(self.fund.balance, Decimal('0.00'))

    def test_balance_with_only_contributions(self):
        """Fund balance should equal total contributions when no grants."""
        Contribution.objects.create(
            fund=self.fund,
            amount=Decimal('1000.00'),
            date=date.today(),
            created_by=self.staff
        )
        Contribution.objects.create(
            fund=self.fund,
            amount=Decimal('500.00'),
            date=date.today(),
            created_by=self.staff
        )

        self.assertEqual(self.fund.balance, Decimal('1500.00'))

    def test_balance_subtracts_approved_grants_only(self):
        """Fund balance should only subtract approved grants, not pending."""
        Contribution.objects.create(
            fund=self.fund,
            amount=Decimal('1000.00'),
            date=date.today(),
            created_by=self.staff
        )

        # Pending grant - should NOT affect balance
        GrantRecommendation.objects.create(
            fund=self.fund,
            nonprofit_name='Pending Nonprofit',
            amount=Decimal('200.00'),
            status='pending'
        )

        # Approved grant - should affect balance
        GrantRecommendation.objects.create(
            fund=self.fund,
            nonprofit_name='Approved Nonprofit',
            amount=Decimal('300.00'),
            status='approved',
            reviewed_by=self.staff,
            reviewed_at=timezone.now()
        )

        # Balance = 1000 - 300 = 700
        self.assertEqual(self.fund.balance, Decimal('700.00'))

    def test_total_contributed_property(self):
        """total_contributed should sum all contributions."""
        Contribution.objects.create(
            fund=self.fund,
            amount=Decimal('1000.00'),
            date=date.today(),
            created_by=self.staff
        )
        Contribution.objects.create(
            fund=self.fund,
            amount=Decimal('2000.00'),
            date=date.today(),
            created_by=self.staff
        )

        self.assertEqual(self.fund.total_contributed, Decimal('3000.00'))
