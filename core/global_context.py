from django.conf import settings
from django.utils import timezone

from apps.risk_manager.utils import get_festive_period


def get_settings(request):
    return {
        'settings': settings,
        'time': timezone.now,
        'utils': {
            'get_festive_period': get_festive_period,
        }
    }