from django.db.models import CASCADE
from django.db.models.base import Model
from django.db.models.fields import TextField, DateTimeField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext as _


class TrackerAlarm(Model):
    tracker = ForeignKey('Tracker', on_delete=CASCADE, verbose_name=_('tracker'))
    message = TextField(verbose_name=_('message'))
    return_message = TextField(verbose_name=_('return message'))
    datetime = DateTimeField(auto_now_add=True, verbose_name=_('datetime'), db_index=True)

    def __str__(self):
        return u'{0}'.format(self.tracker)

    class Meta:
        app_label = 'tracker'
        ordering = ['name', ]
        verbose_name_plural = _('trackers alarms')
        verbose_name = _('tracker alarm')