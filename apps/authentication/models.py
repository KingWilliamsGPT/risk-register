from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    is_super_admin =  models.BooleanField(blank=True, default=False)            # simply implies some common priviledges like elevated actions on risks
    # can_create_other_admins = models.BooleanField(blank=True, default=False)


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
    allow_changable_date_reported = models.BooleanField(blank=True, default=False)
