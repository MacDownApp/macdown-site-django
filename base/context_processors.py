from .models import MacDownVersion


def latest_version(request):
    try:
        latest_version = MacDownVersion.objects.latest('publish_at')
    except MacDownVersion.DoesNotExist:
        latest_version = None
    return {'latest_version': latest_version}
