from django.utils.functional import SimpleLazyObject
from sparkle.models import Application


def get_macdown():
    return Application.objects.get_or_create(slug='macdown')[0]

macdown = SimpleLazyObject(get_macdown)
