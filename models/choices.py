from django.utils.translation import ugettext as _

NULL_AVAILABLE_CHOICES = [
    (True, _('yes').capitalize()),
    (False, _('no').capitalize()),
    (None, '-'),
]

BOOLEAN_CHOICES = [
    (True, _('yes').capitalize()),
    (False, _('no').capitalize()),
]

BATTERY_CHOICES = (
    ('low', 'low'),
    ('medium', 'medium'),
    ('high', 'low'),
)

LONGITUDE_DIRECTION = (
    ('east', _('east').capitalize()),
    ('west', _('west').capitalize()),
)

LATITUDE__DIRECTION = (
    ('south', _('south').capitalize()),
    ('north', _('north').capitalize()),
)