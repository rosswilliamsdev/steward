"""
Setup script to create test users and data for auth testing.
Run with: python manage.py shell < setup_test_users.py
"""
from core.models import CustomUser, Fund, Contribution
from decimal import Decimal
from django.utils import timezone

print("\n=== Setting Up Test Users & Data ===\n")

# 1. Update existing admin user to have is_admin flag
print("1. Updating superuser to have admin flag...")
try:
    admin = CustomUser.objects.get(username='admin')
    admin.is_admin = True
    admin.save()
    print(f"   ✓ Set is_admin=True for {admin.username}")
except CustomUser.DoesNotExist:
    print("   ⚠ No user 'admin' found - creating one...")
    admin = CustomUser.objects.create_superuser(
        username='admin',
        email='admin@steward.org',
        password='admin123',
        is_admin=True
    )
    print(f"   ✓ Created admin user (password: admin123)")

# 2. Create a donor user
print("\n2. Creating donor user...")
donor, created = CustomUser.objects.get_or_create(
    username='donor_alice',
    defaults={
        'email': 'alice@example.com',
        'is_donor': True
    }
)
if created:
    donor.set_password('donor123')
    donor.save()
    print(f"   ✓ Created donor: {donor.username} (password: donor123)")
else:
    donor.is_donor = True
    donor.save()
    print(f"   ✓ Updated existing donor: {donor.username}")

# 3. Create a fund for the donor
print("\n3. Creating fund for donor...")
fund, created = Fund.objects.get_or_create(
    name="Alice Family Foundation",
    donor=donor
)
if created:
    print(f"   ✓ Created fund: {fund.name}")
else:
    print(f"   ✓ Fund already exists: {fund.name}")

# 4. Add some contributions (created by admin)
print("\n4. Adding contributions...")
contrib1, created = Contribution.objects.get_or_create(
    fund=fund,
    amount=Decimal('50000.00'),
    defaults={
        'date': timezone.now().date(),
        'created_by': admin,
        'note': 'Initial contribution'
    }
)
if created:
    print(f"   ✓ Added contribution: ${contrib1.amount}")
else:
    print(f"   ✓ Contribution already exists: ${contrib1.amount}")

contrib2, created = Contribution.objects.get_or_create(
    fund=fund,
    amount=Decimal('25000.00'),
    defaults={
        'date': timezone.now().date(),
        'created_by': admin,
        'note': 'Additional contribution'
    }
)
if created:
    print(f"   ✓ Added contribution: ${contrib2.amount}")
else:
    print(f"   ✓ Contribution already exists: ${contrib2.amount}")

print(f"\n   ✓ Fund balance: ${fund.balance}")

# Summary
print("\n=== Setup Complete ===")
print("\nTest Users:")
print(f"  Admin:  username='admin' password='admin123' (is_admin=True)")
print(f"  Donor:  username='donor_alice' password='donor123' (is_donor=True)")
print(f"\nDonor has 1 fund: '{fund.name}' with balance ${fund.balance}")
print("\nYou can now:")
print("  1. Logout and login as 'admin' to see staff dashboard")
print("  2. Logout and login as 'donor_alice' to see donor dashboard with fund\n")
