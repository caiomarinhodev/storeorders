from django import forms
from django.forms import ModelForm, inlineformset_factory
from app.utils import generate_bootstrap_widgets_for_all_fields

from . import (
    models
)


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone phone'
            if field_name == 'cep' or field_name == 'postalcode':
                field.widget.attrs['class'] = 'form-control cep'


class OrderForm(BaseForm, ModelForm):
    class Meta:
        model = models.Order
        fields = ("id", "client_name", "status", "total_value", "notes")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Order)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)


class OrderFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.Order
        fields = ("id", "client_name", "status", "total_value")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Order)

    def __init__(self, *args, **kwargs):
        super(OrderFormToInline, self).__init__(*args, **kwargs)
