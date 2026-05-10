from django import forms
from django.core.exceptions import ValidationError
from .models import GrantRecommendation, Fund


class GrantRecommendationForm(forms.ModelForm):
    class Meta:
        model = GrantRecommendation
        fields = ['fund', 'nonprofit_name', 'amount', 'memo']
        widgets = {
            'memo': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter fund choices to only show current user's funds
        if self.user:
            self.fields['fund'].queryset = Fund.objects.filter(donor=self.user)

        # Add Tailwind CSS classes to form fields
        self.fields['fund'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-transparent'
        })
        self.fields['nonprofit_name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-transparent',
            'placeholder': 'Enter nonprofit name'
        })
        self.fields['amount'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-transparent',
            'placeholder': '0.00'
        })
        self.fields['memo'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-transparent',
            'placeholder': 'Optional note about this grant recommendation'
        })

    def clean(self):
        cleaned_data = super().clean()
        fund = cleaned_data.get('fund')
        amount = cleaned_data.get('amount')

        if fund and amount:
            if amount > fund.balance:
                raise ValidationError(
                    f"Amount exceeds available balance of ${fund.balance:,.2f}"
                )

        return cleaned_data
