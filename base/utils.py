from sparkle.models import Version


class MacDown(object):
    objects = Version.objects.filter(application__slug='macdown')
