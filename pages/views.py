from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'pages/home.html'


class FeaturesView(TemplateView):
    template_name = 'pages/features.html'


class FAQView(TemplateView):
    template_name = 'pages/faq.html'


home = HomeView.as_view()
features = FeaturesView.as_view()
faq = FAQView.as_view()
