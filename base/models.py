from sparkle.models import Application


def get_macdown():
    return Application.objects.get(slug='macdown')
