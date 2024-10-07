from django.conf import settings
from django.utils import timezone


def get_settings(request):
    return {
        'settings': settings,
        'time': timezone.now,
    }