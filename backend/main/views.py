from django.views.generic.base import TemplateView

from polls.models import Question


class IndexPageView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_polls"] = Question.objects.all().order_by("-pub_date")[:6]
        return context


class AboutPageView(TemplateView):
    template_name = "main/about.html"
