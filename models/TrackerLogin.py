from django.db import models
from django.db.models.base import Model
from django.db.models.fields import DateTimeField, TextField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext as _


class TrackerLogin(Model):
    tracker = ForeignKey('Tracker', on_delete=models.CASCADE, verbose_name=_('tracker'))
    datetime = DateTimeField(auto_now_add=True, verbose_name=_('datetime'), db_index=True)
    message = TextField(verbose_name=_('message'))
    return_message = TextField(verbose_name=_('return message'))

    def __str__(self):
        return u'{tracker} - {datetime}'.format(tracker=self.tracker, datetime=self.datetime)

    class Meta:
        app_label = 'tracker'
        ordering = ['datetime', ]
        verbose_name_plural = _('tracker logins')
        verbose_name = _('tracker login')