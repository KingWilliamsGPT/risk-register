from random import choice as random_choice
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.templatetags.static import static


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


class Department(models.Model):
    # TODO:
    # - ENSURE a department with members cannot be deleted
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=1500, blank=True, default='')

    def __str__(self):
        return self.name

    def get_code(self):
        return self.code.strip()


class GlobalSettings(models.Model):
    class Meta:
        verbose_name = _("GlobalSetting")
        verbose_name_plural = _("GlobalSettings")

    allow_risk_deadlines = models.BooleanField(blank=True, default=True)
    allow_changable_date_reported = models.BooleanField(blank=True, default=False)
