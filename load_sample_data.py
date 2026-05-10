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
    fund1 = Fund.objects.create(
        name="Chen Family Foundation",
        donor=donor1
    )

    fund2 = Fund.objects.create(
        name="Rodriguez Community Fund",
        donor=donor2
    )

    # Create contributions
    print("Creating contributions...")
    contributions_data = [
        (fund1, "100000.00", "2024-01-15"),
        (fund1, "50000.00", "2024-07-10"),
        (fund1, "25000.00", "2024-12-15"),
        (fund2, "75000.00", "2024-02-20"),
        (fund2, "30000.00", "2024-09-05"),
    ]

    for fund, amount, date_str in contributions_data:
        Contribution.objects.create(
            fund=fund,
            amount=Decimal(amount),
            date=datetime.strptime(date_str, "%Y-%m-%d").date(),
            created_by=staff
        )

    # Create grant recommendations
    print("Creating grant recommendations...")
    grants_data = [
        # Fund 1 grants
        {
            'fund': fund1,
            'nonprofit_name': 'Green Valley Land Trust',
            'amount': '25000.00',
            'status': 'approved',
            'created_at': '2024-10-24T10:00:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2024-10-25T14:30:00Z',
            'staff_note': 'Scheduled for release on Nov 1.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Westside Academy Arts',
            'amount': '12000.00',
            'status': 'pending',
            'created_at': '2024-10-21T09:15:00Z',
            'staff_note': 'Staff verifying 501(c)(3) status update.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Community Health Clinic',
            'amount': '50000.00',
            'status': 'approved',
            'created_at': '2024-10-18T11:30:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2024-10-19T10:00:00Z',
            'staff_note': 'Acknowledgement letter received.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Local Food Pantry Network',
            'amount': '8500.00',
            'status': 'approved',
            'created_at': '2024-09-12T14:45:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2024-09-13T09:20:00Z',
            'staff_note': 'Grant distributed via check on 9/20.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Youth Literacy Foundation',
            'amount': '15000.00',
            'status': 'approved',
            'created_at': '2024-08-05T10:20:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2024-08-06T15:00:00Z',
            'staff_note': 'Impact report expected in December.'
        },
        {
            'fund': fund1,
            'nonprofit_name': 'Senior Center Renovation Fund',
            'amount': '20000.00',
            'status': 'denied',
            'created_at': '2024-07-22T13:10:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2024-07-25T11:30:00Z',
            'staff_note': 'Project budget needs clarification. Donor may resubmit with revised proposal.'
        },
        # Fund 2 grants
        {
            'fund': fund2,
            'nonprofit_name': 'Neighborhood Parks Alliance',
            'amount': '18000.00',
            'status': 'approved',
            'created_at': '2024-10-15T08:45:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2024-10-16T13:15:00Z',
            'staff_note': 'Grant approved. Check prepared for November disbursement.'
        },
        {
            'fund': fund2,
            'nonprofit_name': 'Immigrant Resource Center',
            'amount': '22000.00',
            'status': 'pending',
            'created_at': '2024-10-20T12:00:00Z',
            'staff_note': 'Under review. Additional documentation requested from nonprofit.'
        },
        {
            'fund': fund2,
            'nonprofit_name': "Women's Business Incubator",
            'amount': '30000.00',
            'status': 'approved',
            'created_at': '2024-09-28T15:30:00Z',
            'reviewed_by': staff,
            'reviewed_at': '2024-09-30T10:45:00Z',
            'staff_note': 'Approved. Quarterly impact reports requested.'
        },
    ]

    for grant_data in grants_data:
        created_at = timezone.datetime.fromisoformat(grant_data.pop('created_at').replace('Z', '+00:00'))
        reviewed_at_str = grant_data.pop('reviewed_at', None)
        reviewed_at = None
        if reviewed_at_str:
            reviewed_at = timezone.datetime.fromisoformat(reviewed_at_str.replace('Z', '+00:00'))

        GrantRecommendation.objects.create(
            **grant_data,
            created_at=created_at,
            reviewed_at=reviewed_at
        )

    print("\n✅ Sample data loaded successfully!")
    print("\nTest accounts:")
    print("  Donor 1: username='donor1', password='Admin123!'")
    print("  Donor 2: username='donor2', password='Admin123!'")
    print("  Staff:   username='staff', password='Admin123!'")
    print("\nFund balances:")
    print(f"  Chen Family Foundation: ${fund1.balance:,.2f}")
    print(f"  Rodriguez Community Fund: ${fund2.balance:,.2f}")

if __name__ == '__main__':
    load_sample_data()
