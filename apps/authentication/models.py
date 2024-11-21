import uuid
from random import choice as random_choice
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.templatetags.static import static


def generate_recovery_code():
    return str(uuid.uuid4())[:8]


def reset_or_generate_code(user, how_many=settings.MAX_RECOVERY_CODES):
    if how_many <= 0:
        raise ValueError("The number of recovery codes must be greater than zero.")
    
    user.recovery_codes.all().delete()
    recovery_codes = [UserRecoveryCode(user=user) for _ in range(how_many)]
    UserRecoveryCode.objects.bulk_create(recovery_codes)


class User(AbstractUser):
    # class Meta:
    #     ordering = ['-date_joined']
        
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, related_name='staffs')
    is_super_admin =  models.BooleanField(blank=True, default=False)            # simply implies some common priviledges like elevated actions on risks
    # can_create_other_admins = models.BooleanField(blank=True, default=False)
    profile_pic = models.CharField(max_length=255, default=random_choice(settings.DEFAULT_PROFILE_AVATARS))

    def get_profile_url(self):
        if self.profile_pic.startswith('[') and self.profile_pic.endswith(']'):
            return static(self.profile_pic[1:-1])
        return self.profile_pic

    def get_display_name(self):
        return (f'{self.first_name.strip()} {self.last_name.strip()}'.strip()) or self.get_username()


class UserRecoveryCode(models.Model):
    code = models.CharField(default=generate_recovery_code, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recovery_codes')

    def __str__(self):
        return self.code


class Department(models.Model):
    # TODO:
    # - ENSURE a department with members cannot be deleted
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=1500, blank=True, default='')
    _opened_risks = None
    _closed_risks = None

    def __str__(self):
        return self.name

    def get_code(self):
        return self.code.strip()

    def _init_risks(self):
        if self._closed_risks is None or self._opened_risks is None:
            risks = self.risks.all()
            self._closed_risks = risks.filter(is_closed=True)
            self._opened_risks = risks.filter(is_closed=False)

    def get_opened_risks(self):
        self._init_risks()
        return self._opened_risks.count()

    def get_closed_risks(self):
        self._init_risks()
        return self._closed_risks.count()


class GlobalSettings(models.Model):
    class Meta:
        verbose_name = _("GlobalSetting")
        verbose_name_plural = _("GlobalSettings")

    allow_risk_deadlines = models.BooleanField(blank=True, default=True)
    allow_changable_date_reported = models.BooleanField(blank=True, default=False)



class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    action = models.CharField(max_length=20, )
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)


    def get_unread_activities(self):
        return self.user.activities.filter(is_read=False)
