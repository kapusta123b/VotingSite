from polls.models import Choice, Questions
from django import forms

from django.db import transaction
from django.utils import timezone

class CreatePollForm(forms.ModelForm):

    class Meta:
        model = Questions
        fields = ["category", "question_text"]

    # override the form method
    def save(self, commit=True, user=None):
        
        with transaction.atomic():

            # init question
            instance = super().save(commit=False)
            instance.pub_date = timezone.now()

            if user:
                instance.creator = user

            if commit:
                instance.save()

                choices = self.data.getlist('choices')

                # create choices for instance(question)
                for text in choices:
                    Choice.objects.create(question=instance, choice_text=text.strip())

            return instance
        
        
class VotePollForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Choice.objects.none(), widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)

        self.fields['choice'].queryset = question.choice_set.all()