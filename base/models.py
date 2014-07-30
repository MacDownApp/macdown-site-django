from django.utils.functional import SimpleLazyObject
from sparkle.models import Application


macdown = SimpleLazyObject(lambda: Application.objects.get(slug='macdown'))
