#!/usr/bin/env python
"""
Load sample data into the Steward database.

Usage:
    python load_sample_data.py

Note: All users have password 'Admin123!'
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import CustomUser as User, Fund, Contribution, GrantRecommendation
from decimal import Decimal
from django.utils import timezone
from datetime import datetime

def load_sample_data():
    """Load sample data for development/testing."""

    print("Loading sample data...")

    # Clear existing data (optional - comment out if you want to keep existing data)
    print("Clearing existing data...")
    GrantRecommendation.objects.all().delete()
    Contribution.objects.all().delete()
    Fund.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    # Create users
    print("Creating users...")
    donor1, _ = User.objects.get_or_create(
        username='donor1',
        defaults={
            'email': 'sarah.chen@example.com',
            'first_name': 'Sarah',
            'last_name': 'Chen',
            'is_donor': True
        }
    )
    donor1.set_password('Admin123!')
    donor1.save()

    donor2, _ = User.objects.get_or_create(
        username='donor2',
        defaults={
            'email': 'michael.r@example.com',
            'first_name': 'Michael',
            'last_name': 'Rodriguez',
            'is_donor': True
        }
    )
    donor2.set_password('Admin123!')
    donor2.save()

    staff, _ = User.objects.get_or_create(
        username='staff',
        defaults={
            'email': 'admin@steward.org',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_admin': True,
            'is_staff': True,
            'is_superuser': True
        }
    )
    staff.set_password('Admin123!')
    staff.save()

    # Create funds
    print("Creating funds...")
    # Donor 1 (Sarah Chen) - Multiple funds
    fund1 = Fund.objects.create(
        name="Chen Family Foundation",
        donor=donor1
    )

    fund1b = Fund.objects.create(
        name="Sarah Chen Education Fund",
        donor=donor1
    )

    # Donor 2 (Michael Rodriguez) - Single fund
    fund2 = Fund.objects.create(
        name="Rodriguez Community Fund",
        donor=donor2
    )

    # Create contributions spread over 12 months for balance chart
    # Using dates from June 2025 - May 2026 to match current date
    print("Creating contributions...")
    contributions_data = [
        # Fund 1 - Chen Family Foundation (initial large contribution + monthly additions)
        (fund1, "100000.00", "2025-06-15"),  # Initial large contribution
        (fund1, "5000.00", "2025-07-10"),
        (fund1, "5000.00", "2025-08-15"),
        (fund1, "10000.00", "2025-09-20"),
        (fund1, "5000.00", "2025-10-10"),
        (fund1, "5000.00", "2025-11-15"),
        (fund1, "25000.00", "2025-12-15"),   # Year-end contribution
        (fund1, "5000.00", "2026-01-10"),
        (fund1, "5000.00", "2026-02-10"),
        (fund1, "5000.00", "2026-03-10"),
        (fund1, "5000.00", "2026-04-10"),

        # Fund 1b - Sarah Chen Education Fund
        (fund1b, "50000.00", "2025-07-01"),  # Initial contribution
        (fund1b, "10000.00", "2025-12-20"),  # Year-end contribution
        (fund1b, "5000.00", "2026-03-15"),

        # Fund 2 - Rodriguez Community Fund
        (fund2, "75000.00", "2025-06-20"),
        (fund2, "10000.00", "2025-09-05"),
        (fund2, "20000.00", "2025-12-10"),
        (fund2, "5000.00", "2026-02-15"),
    ]

    for fund, amount, date_str in contributions_data:
        Contribution.objects.create(
            fund=fund,
            amount=Decimal(amount),
            date=datetime.strptime(date_str, "%Y-%m-%d").date(),
            created_by=staff
        )

    # Create grant recommendations spread over time
    # Using dates from June 2025 - May 2026 to match current date
    # Reduced grant amounts to show upward balance trend
    print("Creating grant recommendations...")
    grants_data = [
        # Fund 1 grants - smaller amounts spread across the year
        {
            'fund': fund1,
            'nonprofit_name': 'Youth Literacy Foundation',
            'amount': '3000.00',
            'status': 'approved',
            'created_at': '2025-07-05T10:20:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2025-07-06T15:00:00Z',
            'staff_note': 'Impact report expected in December.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Senior Center Renovation Fund',
            'amount': '2000.00',
            'status': 'approved',
            'created_at': '2025-08-22T13:10:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2025-08-25T11:30:00Z',
            'staff_note': 'Approved for facility improvements.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Local Food Pantry Network',
            'amount': '2500.00',
            'status': 'approved',
            'created_at': '2025-09-12T14:45:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2025-09-13T09:20:00Z',
            'staff_note': 'Grant distributed via check on 9/20.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Community Health Clinic',
            'amount': '4000.00',
            'status': 'approved',
            'created_at': '2025-11-18T11:30:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2025-11-19T10:00:00Z',
            'staff_note': 'Acknowledgement letter received.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Environmental Education Center',
            'amount': '3000.00',
            'status': 'approved',
            'created_at': '2026-02-15T09:15:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2026-02-16T11:00:00Z',
            'staff_note': 'Approved for spring programs.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Community Theater Project',
            'amount': '3500.00',
            'status': 'approved',
            'created_at': '2026-03-28T14:20:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2026-03-29T10:00:00Z',
            'staff_note': 'Approved for summer season programming.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Westside Academy Arts',
            'amount': '5000.00',
            'status': 'pending',
            'created_at': '2026-04-21T09:15:00Z',
            'staff_note': 'Staff verifying 501(c)(3) status update.'
        },

        # Fund 1b grants - Sarah Chen Education Fund
        {
            'fund': fund1b,
            'nonprofit_name': 'Public School STEM Initiative',
            'amount': '8000.00',
            'status': 'approved',
            'created_at': '2025-09-10T11:00:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2025-09-11T10:00:00Z',
            'staff_note': 'Approved for robotics lab equipment.'
        },
        {
            'fund': fund1b,
            'nonprofit_name': 'College Access Network',
            'amount': '6000.00',
            'status': 'approved',
            'created_at': '2026-01-18T14:30:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2026-01-19T09:00:00Z',
            'staff_note': 'Scholarship program approved.'
        },
        {
            'fund': fund1b,
            'nonprofit_name': 'After School Tutoring Alliance',
            'amount': '4500.00',
            'status': 'pending',
            'created_at': '2026-04-28T10:45:00Z',
            'staff_note': 'Under review for summer program.'
        },

        # Fund 2 grants
        {
            'fund': fund2,
            'nonprofit_name': "Women's Business Incubator",
            'amount': '8000.00',
            'status': 'approved',
            'created_at': '2025-09-28T15:30:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2025-09-30T10:45:00Z',
            'staff_note': 'Approved. Quarterly impact reports requested.'
        },
        {
            'fund': fund2,
            'nonprofit_name': 'Neighborhood Parks Alliance',
            'amount': '5000.00',
            'status': 'approved',
            'created_at': '2025-11-15T08:45:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2025-11-16T13:15:00Z',
            'staff_note': 'Grant approved. Check prepared for November disbursement.'
        },
        {
            'fund': fund2,
            'nonprofit_name': 'Immigrant Resource Center',
            'amount': '4000.00',
            'status': 'approved',
            'created_at': '2026-01-20T12:00:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2026-01-22T14:30:00Z',
            'staff_note': 'Approved for language services program.'
        },
        {
            'fund': fund2,
            'nonprofit_name': 'Youth Sports Foundation',
            'amount': '6000.00',
            'status': 'pending',
            'created_at': '2026-04-05T10:00:00Z',
            'staff_note': 'Under review. Additional documentation requested from nonprofit.'
        },
    ]

    for grant_data in grants_data:
        created_at = timezone.datetime.fromisoformat(grant_data.pop('created_at').replace('Z', '+00:00'))
        reviewed_at_str = grant_data.pop('reviewed_at', None)
        reviewed_at = None
        if reviewed_at_str:
            reviewed_at = timezone.datetime.fromisoformat(reviewed_at_str.replace('Z', '+00:00'))

        # Create the grant first (auto_now_add will set created_at to now)
        grant = GrantRecommendation.objects.create(
            **grant_data,
            reviewed_at=reviewed_at
        )

        # Update created_at using update() to bypass auto_now_add
        GrantRecommendation.objects.filter(pk=grant.pk).update(created_at=created_at)

    print("\n✅ Sample data loaded successfully!")
    print("\nTest accounts:")
    print("  Donor 1 (Sarah Chen): username='donor1', password='Admin123!' - Has 2 funds")
    print("  Donor 2 (Michael Rodriguez): username='donor2', password='Admin123!' - Has 1 fund")
    print("  Staff:   username='staff', password='Admin123!'")
    print("\nFund balances:")
    print(f"  Chen Family Foundation: ${fund1.balance:,.2f}")
    print(f"  Sarah Chen Education Fund: ${fund1b.balance:,.2f}")
    print(f"  Rodriguez Community Fund: ${fund2.balance:,.2f}")

if __name__ == '__main__':
    load_sample_data()
