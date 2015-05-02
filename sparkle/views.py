from django.utils.translation import ugettext as _
from django.http import Http404
from django.views.generic.detail import DetailView
from .models import (
    Application, Channel, SystemProfileReport, SystemProfileReportRecord,
)


class ChannelView(DetailView):

    model = Channel
    context_object_name = 'channel'
    slug_url_kwarg = 'channel_slug'
    content_type = 'application/xml'
    template_name = 'sparkle/appcast.xml'

    def get_object(self, queryset=None):
        try:
            self.application = Application.objects.get(
                slug=self.kwargs['app_slug'],
            )
        except Application.DoesNotExist:
            raise Http404(
                _("No {verbose_name} found matching the query").format(
                    verbose_name=Application._meta.verbose_name,
                )
            )
        if self.slug_url_kwarg not in self.kwargs:
            obj = self.application.default_channel
        else:
            obj = super(ChannelView, self).get_object(queryset)
        return obj

    def get_context_data(self, **kwargs):
        data = super(ChannelView, self).get_context_data(**kwargs)
        data.update({
            'application': self.application,
            'active_versions': self.application.active_versions(self.object)
        })
        return data

    def render_to_response(self, context, **response_kwargs):
        """Record system profile reports before we send out the response.
        """
        if self.request.GET:
            # Create a report and records of the keys/values
            report = SystemProfileReport.objects.create(
                ip_address=self.request.META.get('REMOTE_ADDR'),
            )
            for key in self.request.GET:
                SystemProfileReportRecord.objects.create(
                    report=report, key=key, value=self.request.GET[key],
                )
        return super(ChannelView, self).render_to_response(
            context, **response_kwargs
        )


channel = ChannelView.as_view()
