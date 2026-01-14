from django import forms
from orders.models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'company_name', 'area_code', 'phone', 'street_address_1', 'street_address_2', 'zip_code', 'is_business']