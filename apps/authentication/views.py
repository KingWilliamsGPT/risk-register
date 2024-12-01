# import this to require login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

# import this for sending email to user
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, authenticate
from django.views import View
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from urllib.parse import urlparse
from django.conf import settings


from .forms import UserRegistrationForm, UserLoginForm2, RecoveryForm


# Create your views here.

@login_required(login_url='login')
def homepage(request):
    return render(request, 'homepage.html')


class CustomLoginView(View):
    """
    A class-based view for logging in users using email or username.
    """
    template_name = 'authentication/login.html'
    redirect_authenticated_users = "risk_register:home"  # Redirect authenticated users here

    def get_redirect_url(self, request):
        """
        Get the URL the user was trying to access or fall back to the default redirect.
        """
        next_url = request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return next_url
        return self.redirect_authenticated_users

    def get(self, request):
        """
        Handle GET requests by displaying the login form.
        """
        if request.user.is_authenticated:
            return redirect(self.redirect_authenticated_users)
        form = UserLoginForm2()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Handle POST requests by authenticating and logging in the user.
        """
        form = UserLoginForm2(request.POST)

        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            # user = authenticate(request, username=username_or_email, password=password) # this only finds a user by username
            user = User.search_user(username_or_email)
            if user is not None and user.check_password(password):
                login(request, user)  # Log in the authenticated user
                return redirect(self.get_redirect_url(request))  # Redirect to where they were heading
            else:
                form.add_error(None, "Invalid username or password.")  # Add a non-field error
        return render(request, self.template_name, {'form': form})




def register(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # email user with activation link
            current_site = get_current_site(request)
            mail_subject = "Activate your account."

            # the message will render what is written in authentication/email_activation/activate_email_message.html
            message = render_to_string('authentication/email_activation/activate_email_message.html', {
                    'user': form.cleaned_data['username'],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':  default_token_generator.make_token(user),
                })
            to_email = form.cleaned_data['email']
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Account created successfully. Please check your email to activate your account.')
            return redirect('login')
        else:
            messages.error(request, 'Account creation failed. Please try again.')


    return render(request, 'authentication/register.html',{
        'form': form
    })

# to activate user from email
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authentication/email_activation/activation_successful.html')
    else:
        return render(request, 'authentication/email_activation/activation_unsuccessful.html')


class AccountRecoveryWithCode(View):
    form_class = RecoveryForm
    template_name = 'authentication/account_recovery_with_code.html'
    redirect_authenticated_users = "risk_register:home"  # Redirect authenticated users here

    def get_redirect_url(self, request):
        """
        Get the URL the user was trying to access or fall back to the default redirect.
        """
        next_url = request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return next_url
        return self.redirect_authenticated_users

    def get(self, request):
        """
        Handle GET requests by displaying the login form.
        """
        if request.user.is_authenticated:
            return redirect(self.redirect_authenticated_users)
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Handle POST requests by authenticating and logging in the user.
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            codes = form.get_codes()
            username_or_email = form.cleaned_data.get('username')

            # Authenticate the user
            # user = authenticate(request, username=username_or_email, password=password) # this only finds a user by username
            user = User.search_user(username_or_email)
            if user is not None and user.can_authenticate_by_codes(codes):
                login(request, user)  # Log in the authenticated user
                return redirect(self.get_redirect_url(request))  # Redirect to where they were heading
            else:
                form.add_error(None, "The data submitted where invalid or no recovery codes where found.")  # Add a non-field error

        return render(request, self.template_name, {'form': form})