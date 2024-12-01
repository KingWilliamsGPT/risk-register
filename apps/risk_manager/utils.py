from random import choice
from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import now as _now
from django.templatetags.static import static
from datetime import date


from django.core.mail.backends.base import BaseEmailBackend
from pysendpulse.pysendpulse import PySendPulse
from mailgun import Mailgun



EMAIL_THRID_PARTY = 'sendpulse'



def get_festive_period():
    # Define festive periods as tuples of (start_date, end_date, period_name, greeting, image_url)

    now = _now()
    festive_periods = [
        (date(now.year, 12, 1), date(now.year, 12, 26), "Christmas", "Merry Christmas", static("festives/chrismas_hat.png")),
        (date(now.year, 12, 31), date(now.year + 1, 1, 1), "New Year", "Happy New Year", static("festives/fun_girl.png")),
        (date(now.year, 2, 14), date(now.year, 2, 14), "Valentine's Day", "Happy Valentine's Day", static("festives/cupid.png")),
        (date(now.year, 10, 31), date(now.year, 10, 31), "Halloween", "Happy Halloween", static("festives/cat.png")),
        (date(now.year, 11, 23), date(now.year, 11, 23), "Thanksgiving", "Happy Thanksgiving", static("festives/emoji_happy.png")),
        # Add more periods as needed
    ]

    # Get today's date in Django's timezone-aware format
    today = now.date()

    # Check each festive period
    for start, end, name, greeting, url in festive_periods:
        # Adjust end year for year-crossing periods
        if start > end:
            # Handle year-crossing periods by splitting the condition
            if (start <= today or today <= end.replace(year=start.year + 1)):
                return {
                    'name': name,
                    'greeting': greeting,
                    'url': url,
                }
        else:
            if start <= today <= end:
                return {
                    'name': name,
                    'greeting': greeting,
                    'url': url,
                }

    return None



def get_app_permissions(app_name):
    """
    Returns all permissions for a given app name.

    Args:
    app_name (str): The name of the Django app.

    Returns:
    list: A list of tuples containing (codename, name) for each permission.
    """
    try:
        app_config = apps.get_app_config(app_name)
    except LookupError:
        return []  # Return an empty list if the app doesn't exist

    permissions = []
    for model in app_config.get_models():
        content_type = ContentType.objects.get_for_model(model)
        perms = Permission.objects.filter(content_type=content_type)
        permissions.extend([(p.codename, p.name) for p in perms])

    return permissions

# Example usage:
# all_permissions = get_app_permissions('your_app_name')
# for codename, name in all_permissions:
#     print(f"Codename: {codename}, Name: {name}")


def get_app_perms(*app_names):
    permissions = []
    for app_name in app_names:
        permissions.extend([f'{app_name}:{perm}' for perm, _ in get_app_permissions(app_name)])
    return permissions


def render_template(template_name, context):
    """
    Renders a template with the provided context and returns it as a string.

    Args:
        template_name (str): The path to the template to render.
        context (dict): The context dictionary to pass to the template.

    Returns:
        str: The rendered template as a string.
    """
    return render_to_string(template_name, context)


def make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    "Generates a random password with the given length and given allowed_chars"
    # Note that default value of allowed_chars does not have "I" or letters
    # that look like it -- just to avoid confusion.
    return ''.join([choice(allowed_chars) for i in range(length)])



class EmailApi(PySendPulse):

    def __init__(self, *args, **kwargs):
        from django.conf import settings
        user_id, secret = settings.SEND_PULSE_ID, settings.SEND_PULSE_SECRET
        super().__init__(user_id, secret, *args, **kwargs)


    def smtp_send_mail(self, text, subject, from_, html=None, to=(), cc=None, bcc=None, attachments=None, attachments_binary=None):
        return super().smtp_send_mail({
            'text': text,
            'subject': subject,
            'from': from_,
            'html': html or '',
            'to': to,
            'cc': cc,
            'bcc': bcc,
            'attachments': attachments or {},
            'attachments_binary': attachments_binary or {},
        })


class Mailgun(Mailgun):
    pass


def send_mail(subject, text, from_=None, html=None, to=(), cc=None, bcc=None, **kw):
    from django.conf import settings
    from_email = from_ or settings.DEFAULT_FROM_EMAIL

    if EMAIL_THRID_PARTY == 'sendpulse':
        api_client = EmailApi()
        api_client.smtp_send_mail(text, subject, from_email, html, to, cc, bcc)
        return api_client


def send_mail_mailgun(domain, api_key, subject, to, html, display_name="Display Name"):
    import requests
    return requests.post(
    f"https://api.mailgun.net/v3/{domain}/messages",
    auth=("api", api_key),
    data={"from": f"{display_name} <mailgun@{domain}>",
    "to": to,
    "subject": subject,
    "html": html})



class EmailBackend(BaseEmailBackend):
    def send_messages(self, messages):
        '''Note a message has the following attributes 
        ['attach',
         'attach_file',
         'attachments',
         'bcc',
         'body',
         'cc',
         'connection',
         'content_subtype',
         'encoding',
         'extra_headers',
         'from_email',
         'get_connection',
         'message',
         'mixed_subtype',
         'recipients',
         'reply_to',
         'send',
         'subject',
         'to']

        '''
        not_sent=0
        total_msgs=0
        for m in messages:
            total_msgs += 1
            try:
                _send_mail(m.subject, m.message, m.from_email, None, m.to, m.cc, m.bcc)
            except Exception:
                not_sent += 1
        sent_count = total_msgs-not_sent
        return sent_count
