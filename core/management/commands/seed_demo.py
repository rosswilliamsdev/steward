from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Fund, Contribution, GrantRecommendation
from decimal import Decimal
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds demo data for portfolio showcase'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing demo data...')

        # Clear existing non-superuser data
        GrantRecommendation.objects.all().delete()
        Contribution.objects.all().delete()
        Fund.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating demo users...')

        # Create staff user
        staff = User.objects.create_user(
            username='staff',
            password='demo123',
            email='staff@steward.demo',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_admin=True
        )

        # Create donor users
        donor1 = User.objects.create_user(
            username='donor',
            password='demo123',
            email='donor@steward.demo',
            first_name='Jane',
            last_name='Smith',
            is_donor=True
        )

        donor2 = User.objects.create_user(
            username='donor2',
            password='demo123',
            email='donor2@steward.demo',
            first_name='Robert',
            last_name='Johnson',
            is_donor=True
        )

        self.stdout.write('Creating funds...')

        # Create funds
        fund1 = Fund.objects.create(
            name="Smith Family Foundation",
            donor=donor1
        )

        fund2 = Fund.objects.create(
            name="Johnson Education Fund",
            donor=donor2
        )

        self.stdout.write('Creating contributions...')

        # Seed contributions for fund1
        Contribution.objects.create(
            fund=fund1,
            amount=Decimal('50000.00'),
            date=date(2024, 1, 15),
            created_by=staff
        )
        Contribution.objects.create(
            fund=fund1,
            amount=Decimal('25000.00'),
            date=date(2024, 6, 10),
            created_by=staff
        )
        Contribution.objects.create(
            fund=fund1,
            amount=Decimal('10000.00'),
            date=date(2024, 11, 5),
            created_by=staff
        )

        # Seed contributions for fund2
        Contribution.objects.create(
            fund=fund2,
            amount=Decimal('100000.00'),
            date=date(2024, 3, 1),
            created_by=staff
        )
        Contribution.objects.create(
            fund=fund2,
            amount=Decimal('50000.00'),
            date=date(2024, 9, 15),
            created_by=staff
        )

        self.stdout.write('Creating grant recommendations...')

        # Seed grant recommendations for fund1
        GrantRecommendation.objects.create(
            fund=fund1,
            nonprofit_name="Local Food Bank",
            amount=Decimal('5000.00'),
            memo="Monthly meal program support",
            status='approved',
            reviewed_by=staff,
            staff_note="Approved - established nonprofit with strong track record"
        )

        GrantRecommendation.objects.create(
            fund=fund1,
            nonprofit_name="Youth Literacy Program",
            amount=Decimal('3000.00'),
            memo="After-school reading initiative",
            status='pending'
        )

        GrantRecommendation.objects.create(
            fund=fund1,
            nonprofit_name="Community Arts Center",
            amount=Decimal('2500.00'),
            memo="Art supplies for underserved schools",
            status='approved',
            reviewed_by=staff
        )

        # Seed grant recommendations for fund2
        GrantRecommendation.objects.create(
            fund=fund2,
            nonprofit_name="State University Scholarship Fund",
            amount=Decimal('25000.00'),
            memo="Engineering scholarships for first-gen students",
            status='approved',
            reviewed_by=staff
        )

        GrantRecommendation.objects.create(
            fund=fund2,
            nonprofit_name="STEM Education Coalition",
            amount=Decimal('15000.00'),
            memo="K-12 robotics program equipment",
            status='pending'
        )

        self.stdout.write(self.style.SUCCESS('✓ Demo data seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('  Donor: username=donor, password=demo123'))
        self.stdout.write(self.style.SUCCESS('  Staff: username=staff, password=demo123'))
