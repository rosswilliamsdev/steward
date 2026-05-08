from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class DonorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Verify that the current user is authenticated and has donor access.
    """
    def test_func(self):
        return self.request.user.is_donor


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Verify that the current user is authenticated and has admin/staff access.
    """
    def test_func(self):
        return self.request.user.is_admin
