try:
    from django.db.models import GenericIPAddressField
except ImportError:
    # Django 1.6 or earlier. Remove this when dropping support to Django 1.7.
    from django.db.models import IPAddressField as GenericIPAddressField  # noqa
