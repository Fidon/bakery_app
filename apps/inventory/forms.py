from django import forms
from .models import SnackItem


class SnackItemForm(forms.ModelForm):
    class Meta:
        model = SnackItem
        fields = ['name', 'unit', 'price', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError("Item name is required.")
        qs = SnackItem.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A snack item with this name already exists.")
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price