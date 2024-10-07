from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)


class Department(models.Model):
    # TODO:
    # - ENSURE a department with members cannot be deleted
    
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1500, blank=True, default='')


class GlobalSettings(models.Model):
    class Meta:
        verbose_name = _("GlobalSetting")
        verbose_name_plural = _("GlobalSettings")

    allow_risk_deadlines = models.BooleanField(blank=True, default=True)
