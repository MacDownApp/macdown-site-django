from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'pages/home.html'


class FAQView(TemplateView):
    template_name = 'pages/faq.html'


home = HomeView.as_view()
faq = FAQView.as_view()
