import re

from .models import Risk
from django import forms
from djmoney.money import Money
from django.core.exceptions import ValidationError
from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth.forms import PasswordChangeForm


from apps.authentication.models import Department, User
from apps.authentication.forms import UserCreationForm, UserRegistrationForm




def is_strong_password(password):
    """
    Validates the security of a password based on common rules.
    
    Args:
        password (str): The password to validate.
    
    Returns:
        tuple: (bool, list). A boolean indicating if the password is strong,
               and a list of reasons why it is not.
    """
    errors = []

    # Rule 1: Minimum length
    if len(password) < settings.MIN_PASSWORD_LENGTH:
        errors.append("Password must be at least 8 characters long.")

    # Rule 2: Contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one uppercase letter.")

    # Rule 3: Contains at least one lowercase letter
    if not any(char.islower() for char in password):
        errors.append("Password must contain at least one lowercase letter.")

    # Rule 4: Contains at least one digit
    if not any(char.isdigit() for char in password):
        errors.append("Password must contain at least one digit.")

    # Rule 5: Contains at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character (!@#$%^&*(), etc.).")

    # Rule 6: Not too common (use a common password dictionary or pattern check)
    common_passwords = settings.COMMON_PASSWORDS
    if password.lower() in common_passwords:
        errors.append("Password is too common and easy to guess.")

    # If there are no errors, the password is strong
    is_strong = not errors
    return is_strong, errors



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

    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='From Date',
    )

    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='To Date',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_date'].widget.attrs.update({
            'hidden': '',
        })
        self.fields['to_date'].widget.attrs.update({
            'hidden': '',
        })


    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date and from_date > to_date:
            # Swap the dates
            cleaned_data['from_date'], cleaned_data['to_date'] = to_date, from_date

        return cleaned_data


class ProfilePicsMixin:
    def get_profile_pics(self):
        return [
            (static(pic[1:-1]), pic) for pic in settings.DEFAULT_PROFILE_AVATARS
        ]


class StaffFormMixin:
    def clean_email(self):
        email = self.cleaned_data['email'].lower()  # Normalize email to lowercase
        is_updating = self.instance.id is not None #getattr(self, 'is_updating')
        if is_updating:
            staff = self.instance
            if User.objects.exclude(id=staff.id).filter(email=email).exists():
                raise ValidationError('Someone else has this email.')
        else:
            if User.objects.filter(email=email).exists():
                raise ValidationError("A user with this email already exists.")
        return email


class AddStaffForm(StaffFormMixin, ProfilePicsMixin, forms.ModelForm):
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



class UpdateStaffMinimalForm(StaffFormMixin, ProfilePicsMixin, forms.ModelForm):
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


class UpdateStaffImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['uploaded_profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uploaded_profile_pic'].widget.attrs.update({
            'id': 'upload_profile_pic',
            'hidden': '',
        })

class StaffPasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "off"}),
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
    )
    confirm_password = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")

        password_is_strong, password_errors = is_strong_password(new_password)

        if not password_is_strong:
            raise forms.ValidationError(f'Password Not Strong Enough 💪:<br> <ul>{"".join([f"<li>{error}</li>" for error in password_errors if error])}</ul>')

        return cleaned_data

    def save(self, user):
        """
        Update the user's password after validating the form.
        """
        user.set_password(self.cleaned_data["new_password"])
        user.save()
        return user

