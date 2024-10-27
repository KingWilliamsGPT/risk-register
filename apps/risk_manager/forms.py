from .models import Risk
from django import forms
from djmoney.money import Money
from django.core.exceptions import ValidationError
from django.conf import settings
from django.templatetags.static import static


from apps.authentication.models import Department, User
from apps.authentication.forms import UserCreationForm, UserRegistrationForm


class AddRiskMinimalForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['risk_description', 'probability', 'impact', 'risk_owner', 'risk_type']

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
        self.fields['risk_owner'].widget.attrs.update({
            'class': 'form-control',
            'id': 'risk_owner',
        })


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

    def clean_risk_budget(self):
        risk_budget = self.cleaned_data.get('risk_budget')
        
        # Ensure risk_budget is compared to a Money object with 0 value in the same currency
        if risk_budget is not None and risk_budget < Money(0, risk_budget.currency):
            raise ValidationError('Budget cannot be a negative number.')
        
        return risk_budget


class RiskFilterForm(forms.Form):
    risk_type = forms.ChoiceField(choices=[('', 'All')] + Risk.RISK_TYPE_CHOICES, required=False)
    probability = forms.ChoiceField(choices=[('', 'All')] + Risk.PROBABILITY_CHOICES, required=False)
    impact = forms.ChoiceField(choices=[('', 'All')] + Risk.PROBABILITY_CHOICES, required=False)
    is_closed = forms.ChoiceField(choices=[('', 'All'), ('True', 'Closed'), ('False', 'Open')], required=False)
    search_string = forms.CharField(required=False)


class ProfilePicsMixin:
    def get_profile_pics(self):
        return [
            (static(pic[1:-1]), pic) for pic in settings.DEFAULT_PROFILE_AVATARS
        ]

class AddStaffForm(ProfilePicsMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'department', 'is_super_admin']

    # uncomment this if you want to change the class/design of the registration form inputs
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'First Name',
            'required': 'True',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Last Name',
            'required': 'True'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'required': 'True'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
            'required': 'True'
        })
        self.fields['department'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Department',
            'required': 'True'
        })


class UpdateStaffMinimalForm(ProfilePicsMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    # uncomment this if you want to change the class/design of the registration form inputs
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'First Name',
            'required': 'True',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Last Name',
            'required': 'True'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'required': 'True'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
            'required': 'True'
        })



class UpdateStaffProfilePicForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update({
            'id': 'new_profile_pic',
            'hidden': '',
        })