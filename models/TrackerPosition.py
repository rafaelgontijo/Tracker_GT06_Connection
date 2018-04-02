from django.db import models
from django.db.models.base import Model
from django.db.models.fields import DateTimeField, DecimalField, TextField, PositiveIntegerField, CharField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext as _

from .choices import LONGITUDE_DIRECTION, LATITUDE__DIRECTION


class TrackerPosition(Model):
    tracker = ForeignKey('Tracker', on_delete=models.CASCADE, verbose_name=_('tracker'))
    datetime = DateTimeField(auto_now_add=True, verbose_name=_('datetime'), db_index=True)
    latitude = DecimalField(max_digits=9, decimal_places=6, verbose_name=_('latitude'))
    longitude = DecimalField(max_digits=9, decimal_places=6, verbose_name=_('longitude'))
    gps_datetime = DateTimeField(auto_now_add=True, verbose_name=_('datetime'), db_index=True)
    speed = PositiveIntegerField(null=True, blank=True, verbose_name=_('speed'))
    direction_longitude = CharField(max_length=20, null=True, blank=True, choices=LONGITUDE_DIRECTION, verbose_name=_('longitude direction'))
    direction_latitude = CharField(max_length=20, null=True, blank=True, choices=LATITUDE__DIRECTION, verbose_name=_('latitude direction'))
    direction_angle = PositiveIntegerField(null=True, blank=True, verbose_name=_('direction angle'))
    message = TextField(verbose_name=_('message'))

    def __str__(self):
        return u'{tracker} - {datetime}'.format(tracker=self.tracker, datetime=self.datetime)

    class Meta:
        app_label = 'tracker'
        ordering = ['datetime', ]
        verbose_name_plural = _('tracker positions')
        verbose_name = _('tracker position')