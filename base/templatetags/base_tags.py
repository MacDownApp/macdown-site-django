from __future__ import division
from django.utils.translation import ugettext as _
from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


@register.simple_tag(takes_context=True)
def absolute_uri(context, path):
    return context['request'].build_absolute_uri(path)


@register.filter
@stringfilter
def volumize(value):
    try:
        value = float(value)
    except ValueError:
        value = 0
    if value == 0:
        return _('0 bytes')
    elif value == 1:
        return _('1 byte')
    for unit in (_('bytes'), _('KB'), _('MB'), _('GB'),):
        if -1024 < value < 1024:
            return _('{value:3.1f} {unit}').format(value=value, unit=unit)
        value /= 1024
    return '{value:3.1f} {unit}'.format(value=value, unit=_('TB'))
