from sparkle.models import Version


def latest_version(request):
    try:
        latest_version = Version.objects.filter(
            application__slug='macdown'
        ).latest('publish_at')
    except Version.DoesNotExist:
        latest_version = None
    return {'latest_version': latest_version}
