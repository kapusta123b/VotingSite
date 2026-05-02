from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse, reverse_lazy


from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from polls.forms import CreatePollForm
from polls.models import Questions, Choice
from django.db.models import Sum


class MainPollsView(ListView):
    model = Questions
    template_name = "polls/index.html"
    paginate_by = 6
    context_object_name = "questions"

    def get_queryset(self):
        queryset = super().get_queryset()
        
        user = self.request.user
        filter_type = self.request.GET.get("filter")

        # lazy loading JOIN
        queryset = queryset.select_related("category", "creator")

        # init all questions created by user
        if user.is_authenticated and filter_type == "user":
            queryset = queryset.filter(creator_id=user.id)

        if filter_type == "community":
            queryset = queryset.exclude(creator_id=user.id)

        # init all questions voted for by users
        if user.is_authenticated and filter_type == "voted":
            queryset = user.polls_voted.all()

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
        
        # logic for wizard random poll
        if self.request.GET.get('wizard') == '1':
            if self.request.GET.get('refresh') == '1':
                self.request.session['wizard_viewed'] = []
            
            viewed_ids = self.request.session.get('wizard_viewed', [])

            # exclude both those that have been viewed and those that have already been voted for
            exclude_ids = set(viewed_ids) | voted_ids
            
            # get random question
            wizard_question = Questions.objects.exclude(id__in=exclude_ids).order_by('?').first()
            
            if wizard_question:
                viewed_ids.append(wizard_question.id)
                self.request.session['wizard_viewed'] = viewed_ids
                context['wizard_question'] = wizard_question

        context.update(
            {
                "polls_voted_ids": voted_ids,
                "category_slug": self.kwargs.get("category_slug"),
            }
        )
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
        # CreatePollForm form calling method
        self.object = form.save(user=self.request.user)
        return redirect(self.get_success_url())


class DetailPollView(DetailView):
    template_name = "polls/detail.html"
    context_object_name = "question"
    model = Questions
    pk_url_kwarg = "question_id"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        session_key = f"viewed_{obj.id}"

        if not self.request.session.get(session_key):

            Questions.objects.filter(pk=obj.pk).update(views_count=F("views_count") + 1)

            self.request.session[session_key] = True

        return obj


class PollResultView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Questions
    template_name = "polls/results.html"
    pk_url_kwarg = "question_id"
    context_object_name = "question"

    def test_func(self):
        self.question_obj = self.get_object()

        # returns True if the current question is in the user's polls_voted list
        return self.request.user.polls_voted.filter(pk=self.question_obj.pk).exists()

    def handle_no_permission(self):
        # if the user has not voted for the question, redirect to the voting page
        return redirect(
            "polls:detail",
            category_slug=self.question_obj.category.slug,
            question_id=self.question_obj.id,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_votes"] = (
            self.object.choice_set.aggregate(Sum("votes"))["votes__sum"] or 0
        )
        return context


class DeletePollView(LoginRequiredMixin, DeleteView):
    model = Questions
    pk_url_kwarg = "question_id"

    def get_queryset(self):
        # check the user in the session to make sure that he actually created the question
        return super().get_queryset().filter(creator=self.request.user)

    def get_success_url(self):
        return (
            reverse("polls:index", kwargs={"category_slug": self.object.category.slug})
            + "?filter=user&sort=-pub_date"
        )


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
