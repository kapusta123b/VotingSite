from django.views.generic.base import TemplateView

from polls.models import Question


class IndexPageView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["recent_polls"] = Question.objects.all().order_by("-pub_date")[:6]    
        context["polls_voted_ids"] = []
        
        if self.request.user.is_authenticated:
            context["polls_voted_ids"] = self.request.user.polls_voted.values_list(
                "id", flat=True
            )
        
        return context


class AboutPageView(TemplateView):
    template_name = "main/about.html"