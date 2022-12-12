from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import datetime


class URLParameter(models.Model):
    dsp = models.CharField(max_length=256)
    mid = models.CharField(max_length=256)
    ip = models.CharField(max_length=256)
    geo = models.CharField(max_length=256)


class TargetCriteria(models.Model):
    class TargetType(models.TextChoices):
        MID = 'MID', _('Mobile ID')
        GEO = 'GEO', _('Geo-Polygon')
        IP = 'IP', _('IP Address')

    type = models.CharField(max_length=256, choices=TargetType.choices, default=TargetType.MID)
    value = models.CharField(max_length=4096, default='')


class CampaignData(models.Model):
    event_time = models.DateTimeField(default=datetime.now, null=True, blank=True)
    data = models.CharField(max_length=8496, default='')
