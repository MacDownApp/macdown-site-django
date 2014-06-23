from django.core.urlresolvers import Http404
from django.views.generic import RedirectView
from base.models import MacDownVersion


class VersionView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        version_string = kwargs.get('version')
        try:
            version = MacDownVersion.objects.get(short_version=version_string)
        except MacDownVersion.DoesNotExist:
            raise Http404
        else:
            return version.update_url


version = VersionView.as_view()
