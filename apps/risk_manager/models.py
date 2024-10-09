from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from djmoney.models.fields import MoneyField
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model



class Risk(models.Model):
    # TODO: 
    #  - RISK SHOULD BE DUE, OVERDUE, LONG OVERDUE, UNSPECIFIED

    RISK_TYPE_CHOICES = [
        ('Operational Risk', 'Operational Risk'),
        ('Financial Risk', 'Financial Risk'),
        ('Strategic Risk', 'Strategic Risk'),
        ('Compliance/Regulatory Risk', 'Compliance/Regulatory Risk'),
        ('Project Risk', 'Project Risk'),
        ('Technological Risk', 'Technological Risk'),
        ('Environmental Risk', 'Environmental Risk'),
        ('Health & Safety Risk', 'Health & Safety Risk'),
        ('Reputational Risk', 'Reputational Risk'),
        ('Market Risk', 'Market Risk'),
        ('Political Risk', 'Political Risk'),
        ('Social Risk', 'Social Risk'),
        ('Supplier/Vendor Risk', 'Supplier/Vendor Risk'),
        ('Geopolitical Risk', 'Geopolitical Risk'),
        ('Human Resources Risk', 'Human Resources Risk'),
        ('Supply Chain Risk', 'Supply Chain Risk'),
        ('Innovation Risk', 'Innovation Risk'),
        ('Insurance Risk', 'Insurance Risk'),
        ('Customer Satisfaction Risk', 'Customer Satisfaction Risk'),
    ]

    RATING_INFO = {
        '1-2': ('very low', 'light_green'),
        '3-3': ('low', 'light_green'),
        '4-9': ('medium', 'yellow'),
        '10-12': ('high', 'orange'),
        '15-16': ('very high', 'red'),
        '20-25': ('extreme', 'oxblood'),
        '=2=2': ('low', 'light_green'),
    }

    PROBABILITY_CHOICES = [
        (1, '1 - Very Low'),
        (2, '2 - Low'),
        (3, '3 - Medium'),
        (4, '4 - High'),
        (5, '5 - Very High'),
    ]


    RANGE_1_TO_5 = [
            MinValueValidator(1),  # Minimum value of 1
            MaxValueValidator(5)   # Maximum value of 5
        ]

    class Meta:
        verbose_name = _("Risk")
        verbose_name_plural = _("Risks")
        
    implication = models.CharField(max_length=500, blank=True, default='')

    risk_type = models.CharField(max_length=50, choices=RISK_TYPE_CHOICES)
    risk_description = models.CharField(max_length=500, blank=True, default='')
    # category = models.ForeignKey("Category", on_delete=models.CASCADE)from djnago.

    probability = models.PositiveSmallIntegerField(
        choices=PROBABILITY_CHOICES,
        validators=RANGE_1_TO_5,
    )
    impact = models.PositiveSmallIntegerField(
        choices=PROBABILITY_CHOICES,
        validators=RANGE_1_TO_5,
    )


    # Admin section #############################################################################################

    risk_response = models.CharField(max_length=500, blank=True, default='')
    risk_owner = models.ForeignKey("authentication.Department", on_delete=models.CASCADE, related_name='risks')
    risk_budget = MoneyField(max_digits=10, decimal_places=2, default_currency='NGN')

    # completed_actions = models.CharField(max_length=1500, blank=True, null=True)
    # future_actions = models.CharField(max_length=1500, blank=True, null=True)

    is_closed = models.BooleanField(default=False)       # once the risk is closed by an admin it cannot be edited until opened by another admin


    date_opened = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(editable=False, null=True)
    last_update = models.DateTimeField(auto_now=True)
    estimated_closing_date = models.DateTimeField()
    opened_by = models.CharField(max_length=50, blank=True, null=True)
    closed_by = models.DateTimeField(null=True, blank=True)
    

    def rating(self):
        return self.probability * self.impact

    def rating_info(self):
        rating = self.rating()

        info_dict = lambda info: {'tag': info[0], 'color': info[1]}

        for rkey, rating_info in self.RATING_INFO.items():
            if rkey.startswith('='):
                a, b = rkey[1], rkey[3]
                # print(f'a={a} b={b} {self.probability} {self.impact}')
                if str(self.probability) == a and str(self.impact) == b:
                    return info_dict(rating_info)
            else:
                a, b = rkey.split('-', 1)
                if rating in range(int(a), int(b)+1):
                    return info_dict(rating_info)
        
        # return info_dict((None, None))

    def is_overdue(self):
        # suggested query: find Risk(opened=True. estimated_closing_date<=today)
        if self.is_opened and self.estimated_closing_date is None and timezone.now() >= self.estimated_closing_date:
            return True
        



