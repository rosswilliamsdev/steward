"""
Test script to verify Steward models work as designed.
Run with: python manage.py shell < test_models.py
"""
from core.models import CustomUser, Fund, Contribution, GrantRecommendation
from decimal import Decimal
from django.utils import timezone

print("\n=== Testing Steward Models ===\n")

# Clean up any existing test data
print("0. Cleaning up existing test data...")
# Delete in reverse order of dependencies: grants -> contributions -> funds -> users
GrantRecommendation.objects.filter(fund__donor__username='john_donor').delete()
Contribution.objects.filter(fund__donor__username='john_donor').delete()
Fund.objects.filter(donor__username='john_donor').delete()
CustomUser.objects.filter(username__in=['john_donor', 'staff_jane']).delete()
print("   ✓ Cleanup complete\n")

# Create a donor user
print("1. Creating donor user...")
donor = CustomUser.objects.create_user(
    username='john_donor',
    email='john@example.com',
    password='testpass123',
    is_donor=True,
    is_admin=False
)
print(f"   ✓ Created donor: {donor.username} (is_donor={donor.is_donor})")

# Create a staff admin
print("\n2. Creating staff admin...")
staff = CustomUser.objects.create_user(
    username='staff_jane',
    email='jane@steward.org',
    password='testpass123',
    is_donor=False,
    is_admin=True
)
print(f"   ✓ Created staff: {staff.username} (is_admin={staff.is_admin})")

# Create a fund
print("\n3. Creating fund for donor...")
fund = Fund.objects.create(
    name="Smith Family Education Fund",
    donor=donor
)
print(f"   ✓ Created fund: {fund.name}")
print(f"   ✓ Initial balance: ${fund.balance}")

# Add contributions
print("\n4. Adding contributions...")
contrib1 = Contribution.objects.create(
    fund=fund,
    amount=Decimal('10000.00'),
    date=timezone.now().date(),
    created_by=staff
)
print(f"   ✓ Added contribution: ${contrib1.amount}")

contrib2 = Contribution.objects.create(
    fund=fund,
    amount=Decimal('5000.00'),
    date=timezone.now().date(),
    created_by=staff
)
print(f"   ✓ Added contribution: ${contrib2.amount}")
print(f"   ✓ Fund balance after contributions: ${fund.balance}")

# Create grant recommendations
print("\n5. Creating grant recommendations...")
grant1 = GrantRecommendation.objects.create(
    fund=fund,
    nonprofit_name="Local Library Foundation",
    amount=Decimal('2000.00'),
    memo="New children's books"
)
print(f"   ✓ Created grant: {grant1.nonprofit_name} - ${grant1.amount} (status: {grant1.status})")

grant2 = GrantRecommendation.objects.create(
    fund=fund,
    nonprofit_name="Community College Scholarship Program",
    amount=Decimal('8000.00'),
    memo="Student scholarships"
)
print(f"   ✓ Created grant: {grant2.nonprofit_name} - ${grant2.amount} (status: {grant2.status})")

# Test balance with pending grants (should not affect balance)
print(f"\n   ✓ Fund balance (grants still pending): ${fund.balance}")

# Approve one grant
print("\n6. Testing grant approval workflow...")
grant1.status = 'approved'
grant1.reviewed_by = staff
grant1.staff_note = "Approved - aligns with fund mission"
grant1.save()
print(f"   ✓ Approved grant to {grant1.nonprofit_name}")
print(f"   ✓ Fund balance after approval: ${fund.balance}")

# Deny the other grant
grant2.status = 'denied'
grant2.reviewed_by = staff
grant2.staff_note = "Does not align with education focus"
grant2.save()
print(f"   ✓ Denied grant to {grant2.nonprofit_name}")
print(f"   ✓ Fund balance (denied grant should not affect): ${fund.balance}")

# Summary
print("\n=== Summary ===")
print(f"Total contributions: ${sum(c.amount for c in fund.contributions.all())}")
print(f"Approved grants: ${sum(g.amount for g in fund.grant_recommendations.filter(status='approved'))}")
print(f"Expected balance: $13,000.00 (15,000 - 2,000)")
print(f"Actual balance: ${fund.balance}")
print(f"\n✓ All model operations completed successfully!")
