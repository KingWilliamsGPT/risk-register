from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django import forms

from .models import Department


User = get_user_model()

# uncomment this if you want to change the class/design of the login form
class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'required': 'True',
            'id': 'username_field',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'True'
        })


class UserLoginForm2(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username or Email',
            'required': 'True',
            'id': 'username_field',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'True'
        })

# Customizing Registration Form from UserCreationForm
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    # uncomment this if you want to change the class/design of the registration form inputs
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
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
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'True',
            'id': 'password1',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Retype Password',
            'required': 'True',
            'id': 'password2'
        })


class ResetPasswordForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
            'required': 'True',
            'id': 'email_field',
        })


class ResetPasswordConfirmForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ResetPasswordConfirmForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New Password',
            'required': 'True'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Retype New Password',
            'required': 'True'
        })


class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'required': 'true',
            'id': 'dept_name',
            'placeholder': 'eg. Financial Department',
        })

        self.fields['code'].widget.attrs.update({
            'class': 'form-control',
            'id': 'dept_code',
            'required': 'true',
            'placeholder': 'eg. FIN-DEPT'
        })

        mx = Department.description.field.max_length
        self.fields['description'].widget = forms.Textarea()  
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'id': 'dept_desc',
            'placeholder': f'brief description of department, max characters {mx}',
            'maxlength': str(mx),
        })


class RecoveryForm(forms.Form):
    username = forms.CharField()
    code1 = forms.CharField()
    code2 = forms.CharField()
    code3 = forms.CharField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username or Email',
            'required': 'True',
            'id': 'username_field',
        })
        self.fields['code1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'code 1',
            'required': 'True',
        })
        self.fields['code2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'code 2',
            'required': 'True',
        })
        self.fields['code3'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'code 3',
            'required': 'True',
        })

    def _clean(self, code):
        return code.strip()

    def clean_code1(self):
        return self._clean(self.cleaned_data.get('code1'))

    def clean_code2(self):
        return self._clean(self.cleaned_data.get('code2'))

    def clean_code3(self):
        return self._clean(self.cleaned_data.get('code3'))

    def get_codes(self):
        return [self.cleaned_data.get(code) for code in ('code1', 'code2', 'code3')]