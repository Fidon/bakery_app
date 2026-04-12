from django import forms
from apps.inventory.models import SnackItem


class SaleItemForm(forms.Form):
    """Validates a single line item in the cart."""
    snack_item = forms.ModelChoiceField(
        queryset=SnackItem.objects.filter(is_active=True),
        error_messages={'invalid_choice': 'Selected item is invalid or inactive.'}
    )
    quantity = forms.IntegerField(
        min_value=1,
        error_messages={
            'min_value': 'Quantity must be at least 1.',
            'invalid': 'Enter a valid quantity.',
        }
    )

    def clean_snack_item(self):
        item = self.cleaned_data.get('snack_item')
        if item and not item.is_active:
            raise forms.ValidationError('This item has been deactivated.')
        return item