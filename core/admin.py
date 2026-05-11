from django.contrib import admin
from .models import Fund, Contribution, GrantRecommendation


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('name', 'donor', 'balance_display', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'donor__username', 'donor__email')
    readonly_fields = ('balance_display', 'created_at')

    @admin.display(description='Current Balance')
    def balance_display(self, obj):
        return f"${obj.balance:,.2f}"


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('fund', 'amount', 'date', 'created_by', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('fund__name', 'fund__donor__username', 'note')
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on new contributions
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(GrantRecommendation)
class GrantRecommendationAdmin(admin.ModelAdmin):
    list_display = ('nonprofit_name', 'fund', 'amount', 'status', 'created_at', 'reviewed_by')
    list_filter = ('status', 'created_at', 'reviewed_at')
    search_fields = ('nonprofit_name', 'fund__name', 'fund__donor__username', 'memo')
    readonly_fields = ('created_at', 'reviewed_at')

    fieldsets = (
        ('Grant Information', {
            'fields': ('fund', 'nonprofit_name', 'amount', 'memo')
        }),
        ('Status', {
            'fields': ('status', 'reviewed_by', 'staff_note')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'reviewed_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # Auto-set reviewed_by and reviewed_at when status changes to approved/denied
        if change and 'status' in form.changed_data:
            if obj.status in ['approved', 'denied']:
                obj.reviewed_by = request.user
                from django.utils import timezone
                obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)
