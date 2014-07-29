from django.http import Http404
from django.views.generic import RedirectView, ListView
from sparkle.models import Version
from base.models import macdown


class VersionView(RedirectView):

    permanent = False

    def get_version(self, **kwargs):
        try:
            return macdown.versions.get(**kwargs)
        except Version.DoesNotExist:
            raise Http404

    def get_redirect_url(self, *args, **kwargs):
        return self.get_version(**kwargs).update_url


class LatestVersionView(VersionView):
    def get_version(self, **kwargs):
        return macdown.active_versions().latest()


version = VersionView.as_view()
latest = LatestVersionView.as_view()
