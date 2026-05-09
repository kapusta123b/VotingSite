from django.views.generic.detail import SingleObjectMixin
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView

from django.contrib import messages

from django.urls import reverse

from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from polls.forms import CreatePollForm, VotePollForm
from polls.models import Question


class MainPollsView(ListView):
    model = Question
    template_name = "polls/index.html"
    paginate_by = 6
    context_object_name = "questions"

    def get_queryset(self):
        user = self.request.user
        filter_type = self.request.GET.get("filter")

        if filter_type == "user":
            queryset = Question.objects.user_polls(user)

        elif filter_type == "voted" and user.is_authenticated:
            queryset = user.polls_voted.all()

        else:
            queryset = Question.objects.community_polls(user)

        return (
            queryset.select_related("category", "creator")
            .by_category(self.kwargs.get('category_slug'))
            .sorted_by(self.request.GET.get("sort"))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voted_ids = self.model.voted_ids(self.request.user)
        
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
        messages.success(self.request, "Poll created successfully!")

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
    model = Question
    pk_url_kwarg = "question_id"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_views(self.request.session)
        
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voted_ids = self.model.voted_ids(self.request.user)

        context["form"] = VotePollForm(question=self.object)
        context["voted_ids"] = voted_ids 
        context["similar_polls"] = self.object.similar_polls(self.request.user)
        
        return context
    


class ResultPollView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Question
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


class DeletePollView(LoginRequiredMixin, DeleteView):
    model = Question
    pk_url_kwarg = "question_id"

    def get_queryset(self):
        # check the user in the session to make sure that he actually created the question
        return super().get_queryset().filter(creator=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Poll deleted successfully!")

        return (
            reverse("polls:index", kwargs={"category_slug": self.object.category.slug})
            + "?filter=user&sort=-pub_date"
        )


class PollVoteView(LoginRequiredMixin, FormView, SingleObjectMixin):
    model = Question
    pk_url_kwarg = 'question_id'
    form_class = VotePollForm
    template_name = 'polls/detail.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        self.object = kwargs['question'] = self.get_object()

        return kwargs
    
    def form_valid(self, form):
        vote_success = self.object.vote(self.object.id,self.request.user, form.cleaned_data['choice'])
        (
            messages.success(self.request, "Your vote has been recorded!")
            if vote_success 
            else 
            messages.warning(self.request, "You have already voted for this poll!")
        )

        return super().form_valid(form)
        
    def get_success_url(self):
        question_category_slug = self.object.category.slug
        question_id = self.object.id

        

        return reverse("polls:results", kwargs={
            "category_slug": question_category_slug,
            "question_id": question_id,
        })