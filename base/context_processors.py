from sparkle.models import Channel, Version
from .models import macdown


def latest_version(request):
    try:
        latest_version = macdown.active_versions().latest()
    except Version.DoesNotExist:
        latest_version = None
    return {'latest_version': latest_version}


def channels(request):
    return {'channels': Channel.objects.all()}
