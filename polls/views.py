from django.contrib.auth.decorators import login_required

from django.utils import timezone

from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import DetailView, ListView

from polls.forms import CreatePollForm
from polls.models import Questions, Choice
from django.db.models import Sum

class MainPollsView(ListView):
    model = Questions
    template_name = 'polls/index.html'
    paginate_by = 6
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polls_voted_ids = []

        if self.request.user.is_authenticated:
            polls_voted_ids = self.request.user.polls_voted.values_list('id', flat=True)

        context['polls_voted_ids'] = polls_voted_ids
        
        category_slug = self.kwargs.get('category_slug')
        context['category_slug'] = category_slug
        return context

    def get_queryset(self):
        queryset = Questions.objects.select_related('category').all()
        category_slug = self.kwargs.get('category_slug')
        
        if category_slug and category_slug != 'all':
            return queryset.filter(category__slug=category_slug)
        return queryset
        

@login_required
def create_poll(request):
    if request.method == 'POST':
        form = CreatePollForm(data=request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.creator = request.user
            question.pub_date = timezone.now()
            question.save()

            choices_list = request.POST.getlist('choice')

            for choice_text in choices_list:
                if choice_text.strip():
                    Choice.objects.create(question=question, choice_text=choice_text)

            return redirect('polls:index', 'all')

    else:
        form = CreatePollForm()

    return render(request, 'polls/create_poll.html', context={'form': form})

class DetailPollView(DetailView):
    template_name = 'polls/detail.html'
    context_object_name = 'question'

    def get_object(self, queryset=None):
        question_id = self.kwargs.get('question_id')

        question = get_object_or_404(Questions, pk=question_id)
        question.views_count += 1
        question.save()

        return question

def results(request, question_id, category_slug=None):
    question = get_object_or_404(Questions, pk=question_id)

    total_votes = question.choice_set.aggregate(Sum('votes'))['votes__sum'] or 0
    return render(request, 'polls/results.html', {
        'question': question,
        'total_votes': total_votes
    })


@login_required
def vote(request, question_id, category_slug=None):
    questions = get_object_or_404(Questions, pk=question_id)

    if questions in request.user.polls_voted.all():
        return redirect('polls:results', questions.category.slug, questions.id)

    user = request.user

    try:
        selected_choice = questions.choice_set.get(pk=request.POST['choice'])
    
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'questions': questions,
            'error_message': "You didn't select a choice.",
        })

    selected_choice.votes += 1
    selected_choice.save()

    user.votes += 1
    user.save()
    user.polls_voted.add(questions)

    return redirect('polls:results', questions.category.slug, questions.id)