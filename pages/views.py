from django.http import Http404
from django.template.base import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'pages/home.html'


class PageView(TemplateView):

    def get(self, request, *args, **kwargs):
        self.name = kwargs['name']
        return super(PageView, self).get(request, *args, **kwargs)

    def get_template_names(self):
        template_name = 'pages/{name}.html'.format(name=self.name)
        try:
            get_template(template_name)
        except TemplateDoesNotExist:
            raise Http404
        return [template_name]


home = HomeView.as_view()
page = PageView.as_view()
