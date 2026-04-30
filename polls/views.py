from django.contrib.auth.decorators import login_required
from django.db.models import F
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

    def get_queryset(self):
        user = self.request.user
        filter_type = self.request.GET.get("filter")
        
        # init all questions voted for by users
        if user.is_authenticated and filter_type == "voted":
            queryset = user.polls_voted.all()

        else:
            queryset = Questions.objects.all()

        # lazy loading JOIN
        queryset = queryset.select_related("category", "creator")

        # init all questions created by user
        if user.is_authenticated and filter_type == "user":
            queryset = queryset.filter(creator=user)

        # sort by category
        category_slug = self.kwargs.get("category_slug")
        if category_slug and category_slug != "all":
            queryset = queryset.filter(category__slug=category_slug)

        # sort by option
        sort = self.request.GET.get("sort", "-pub_date")
        return queryset.order_by("?" if sort == "random" else sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # use set for instant (O(1)) pattern lookup
        voted_ids = set()
        if self.request.user.is_authenticated:
            voted_ids = set(self.request.user.polls_voted.values_list("id", flat=True))

        context.update({
            "polls_voted_ids": voted_ids,
            "category_slug": self.kwargs.get("category_slug"),
        })
        return context


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

            Questions.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)

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
