import re

from django.db.models import CASCADE
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _


class Tracker(Model):
    user = ForeignKey('auth.User', on_delete=CASCADE, verbose_name=_('user'))
    name = CharField(max_length=150, verbose_name=_('name'))
    imei = CharField(max_length=100, verbose_name=_('imei'), db_index=True, unique=True)
    phone = CharField(max_length=20, verbose_name=_('number'))
    model = ForeignKey('TrackerModel', null=True, on_delete=CASCADE, verbose_name=_('model'))

    def __str__(self):
        return u'{0}'.format(self.name)

    def set_phone(self):
        self.phone = re.sub("[^0123456789]", "", self.phone)

    class Meta:
        app_label = 'tracker'
        ordering = ['name', ]
        verbose_name_plural = _('trackers')
        verbose_name = _('tracker')


@receiver(pre_save, sender=Tracker)
def set_tracker_pre_save(sender, instance, *args, **kwargs):
    instance.set_number()


class TrackerBrand(Model):
    name = CharField(max_length=150, verbose_name=_('name'))

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        app_label = 'tracker'
        ordering = ['name', ]
        verbose_name_plural = _('trackers brands')
        verbose_name = _('tracker brand')


class TrackerModel(Model):
    brand = ForeignKey('TrackerBrand', null=True, on_delete=CASCADE, verbose_name=_('brand'))
    name = CharField(max_length=150, verbose_name=_('name'))

    def __str__(self):
        return u'{brand} - {model}'.format(brand=self.brand.name, model=self.name)

    class Meta:
        app_label = 'tracker'
        ordering = ['name', ]
        verbose_name_plural = _('trackers models')
        verbose_name = _('tracker model')