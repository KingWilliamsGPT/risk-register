from .models import Risk
from django import forms


class AddRiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['risk_description'].widget = forms.Textarea()  
        self.fields['risk_description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Outline the risk: What could go wrong and how might it affect us.',
            'id': 'risk_description',
            'rows': '3',
            'required': 'true',
        })
        self.fields['risk_type'].widget.attrs.update({
            'class': 'form-control',
            'id': 'risk_type',
        })
        self.fields['probability'].widget.attrs.update({
            'class': 'form-control',
            'id': 'probability',
        })
        self.fields['impact'].widget.attrs.update({
            'class': 'form-control',
            'id': 'impact',
        })
        self.fields['risk_response'].widget = forms.Textarea()  
        self.fields['risk_response'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'How this risk should be tackled, what\'s been done',
            'id': 'risk_response',
            'rows': '3',
        })
        self.fields['risk_owner'].widget.attrs.update({
            'class': 'form-control',
            'id': 'risk_owner',
        })
        self.fields['risk_budget'].widget.attrs.update({
            'class': 'form-control',
            'id': 'risk_budget',
        })
        self.fields['is_closed'].widget.attrs.update({
            'class': 'form-check-input',
            'id': 'is_closed',
            'data-toggle': "toggle",
        })


class RiskFilterForm(forms.Form):
    risk_type = forms.ChoiceField(choices=[('', 'All')] + Risk.RISK_TYPE_CHOICES, required=False)
    probability = forms.ChoiceField(choices=[('', 'All')] + Risk.PROBABILITY_CHOICES, required=False)
    impact = forms.ChoiceField(choices=[('', 'All')] + Risk.PROBABILITY_CHOICES, required=False)
    is_closed = forms.ChoiceField(choices=[('', 'All'), ('True', 'Closed'), ('False', 'Open')], required=False)