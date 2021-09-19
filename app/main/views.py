from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class HomepageView(LoginRequiredMixin, TemplateView):
    template_name = "app.html"
