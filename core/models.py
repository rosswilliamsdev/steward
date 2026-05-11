from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from decimal import Decimal


class CustomUser(AbstractUser):
    is_donor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class Fund(models.Model):
    name = models.CharField(max_length=200)
    donor = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='funds',
        limit_choices_to={'is_donor': True}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance(self):
        contributed = self.contributions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        granted = self.grant_recommendations.filter(
            status='approved'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        return contributed - granted

    @property
    def total_contributed(self):
        """Total amount contributed to this fund."""
        return self.contributions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Contribution(models.Model):
    fund = models.ForeignKey(
        Fund,
        on_delete=models.PROTECT,
        related_name='contributions'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True)
    date = models.DateField()
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='contributions_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fund.name} - ${self.amount} on {self.date}"

    class Meta:
        ordering = ['-date']


class GrantRecommendation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]

    fund = models.ForeignKey(
        Fund,
        on_delete=models.PROTECT,
        related_name='grant_recommendations'
    )
    nonprofit_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    staff_note = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grants_reviewed'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nonprofit_name} - ${self.amount} ({self.status})"

    class Meta:
        ordering = ['-created_at']