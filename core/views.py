from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


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
