from django.http import Http404
from django.template.base import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import TemplateView

from .utils import get_language_infos


class HomeView(TemplateView):
    template_name = 'pages/home.html'


class PageView(TemplateView):

    def get(self, request, *args, **kwargs):
        self.name = kwargs['name']
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        template_name = 'pages/{name}.html'.format(name=self.name)
        try:
            get_template(template_name)
        except TemplateDoesNotExist:
            raise Http404
        return [template_name]


class FeaturesView(TemplateView):

    template_name = 'pages/features.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['language_infos'] = get_language_infos()
        return data


home = HomeView.as_view()
page = PageView.as_view()
features = FeaturesView.as_view()
