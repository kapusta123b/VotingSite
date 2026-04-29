from django.contrib.auth.decorators import login_required

from django.urls import reverse

from django.utils import timezone

from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from polls.forms import CreatePollForm
from polls.models import Questions, Choice
from django.db.models import Sum


class MainPollsView(ListView):
    model = Questions
    template_name = "polls/index.html"
    paginate_by = 6
    context_object_name = "questions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polls_voted_ids = []

        if self.request.user.is_authenticated:
            polls_voted_ids = self.request.user.polls_voted.values_list("id", flat=True)

        context["polls_voted_ids"] = polls_voted_ids

        category_slug = self.kwargs.get("category_slug")
        context["category_slug"] = category_slug
        return context

    def get_queryset(self):
        queryset = Questions.objects.select_related("category")

        sort_by = self.request.GET.get("sort", "-pub_date")
        queryset = queryset.order_by("?" if sort_by == "random" else sort_by)

        filter_key = self.request.GET.get("filter")
        filters = {
            "user": (
                {"creator": self.request.user}
                if self.request.user.is_authenticated
                else {}
            ),
            "community": {},
        }
        queryset = queryset.filter(**filters.get(filter_key, {}))

        category_slug = self.kwargs.get("category_slug")
        if category_slug and category_slug != "all":
            queryset = queryset.filter(category__slug=category_slug)

        return queryset


class CreatePollView(LoginRequiredMixin, CreateView):
    form_class = CreatePollForm
    template_name = "polls/create_poll.html"

    def get_success_url(self):
        return (
            reverse("polls:index", kwargs={"category_slug": self.object.category.slug})
            + "?filter=user&sort=-pub_date"
        )

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.pub_date = timezone.now()

        response = super().form_valid(form)

        choices_list = self.request.POST.getlist("choice")

        for choice_text in choices_list:
            if choice_text.strip():
                Choice.objects.create(question=self.object, choice_text=choice_text)

        return response


class DetailPollView(DetailView):
    template_name = "polls/detail.html"
    context_object_name = "question"
    model = Questions
    pk_url_kwarg = "question_id"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        session_key = f"viewed_{obj.id}"

        if not self.request.session.get(session_key):

            obj.views_count += 1
            obj.save()

            self.request.session[session_key] = True

        return obj


class PollResultView(DetailView):
    model = Questions
    template_name = "polls/results.html"
    pk_url_kwarg = "question_id"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_votes"] = (
            self.object.choice_set.aggregate(Sum("votes"))["votes__sum"] or 0
        )
        return context
    

class DeletePollView(DeleteView):
    pass


@login_required
def vote(request, question_id, category_slug=None):
    questions = get_object_or_404(Questions, pk=question_id)

    if questions in request.user.polls_voted.all():
        return redirect("polls:results", questions.category.slug, questions.id)

    user = request.user

    try:
        selected_choice = questions.choice_set.get(pk=request.POST["choice"])

    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "questions": questions,
                "error_message": "You didn't select a choice.",
            },
        )

    selected_choice.votes += 1
    selected_choice.save()

    user.votes += 1
    user.save()
    user.polls_voted.add(questions)

    return redirect("polls:results", questions.category.slug, questions.id)
