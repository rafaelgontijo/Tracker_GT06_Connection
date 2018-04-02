from django.db.models import CASCADE
from django.db.models.base import Model
from django.db.models.fields import TextField, DateTimeField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext as _


class TrackerAlivePacket(Model):
    tracker = ForeignKey('Tracker', on_delete=CASCADE, verbose_name=_('tracker'))
    terminal_information = TextField(verbose_name=_('information'))
    message = TextField(verbose_name=_('message'))
    return_message = TextField(verbose_name=_('return message'))
    datetime = DateTimeField(auto_now_add=True, verbose_name=_('datetime'), db_index=True)

    def __str__(self):
        return u'{0}'.format(self.tracker)

    class Meta:
        app_label = 'tracker'
        ordering = ['tracker', ]
        verbose_name_plural = _('trackers alive packets')
        verbose_name = _('tracker alive packet')