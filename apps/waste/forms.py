from django import forms
from apps.inventory.models import SnackItem


class WasteReportForm(forms.Form):
    snack_item = forms.ModelChoiceField(
        queryset=SnackItem.objects.filter(is_active=True).order_by('name'),
        empty_label='Select snack item',
        error_messages={'required': 'Please select a snack item.', 'invalid_choice': 'Please select a valid snack item.'},
    )
    quantity = forms.IntegerField(
        min_value=1,
        error_messages={
            'required': 'Quantity is required.',
            'invalid': 'Enter a valid whole number for quantity.',
            'min_value': 'Quantity must be at least 1.',
        },
    )
    reason = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 3}),
        error_messages={'required': 'Reason for waste is required.'},
    )
    waste_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'required': 'Waste date is required.', 'invalid': 'Enter a valid date.'},
    )

    def clean_reason(self):
        reason = self.cleaned_data.get('reason', '')
        if not reason.strip():
            raise forms.ValidationError('Reason for waste is required.')
        return reason.strip()