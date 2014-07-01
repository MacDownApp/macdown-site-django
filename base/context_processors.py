from sparkle.models import Version
from .models import get_macdown


def latest_version(request):
    try:
        latest_version = get_macdown().active_versions().latest()
    except Version.DoesNotExist:
        latest_version = None
    return {'latest_version': latest_version}
