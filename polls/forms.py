from polls.models import Choice, Question
from django import forms

from django.db import transaction
from django.utils import timezone

class CreatePollForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ["category", "question_text"]

    def clean(self):
        cleaned_data = super().clean()
        choices = [c.strip() for c in self.data.getlist('choices') if c.strip()]
        
        if len(choices) < 2:
            raise forms.ValidationError("The poll must contain at least 2 answer options.")
            
        cleaned_data['choices_list'] = choices 
        return cleaned_data

    def save(self, user=None):
        with transaction.atomic():
            instance = super().save(commit=False)

            if user:
                instance.creator = user

            instance.save()

            choices = self.cleaned_data.get('choices_list', [])
            for text in choices:
                Choice.objects.create(question=instance, choice_text=text)
            
            return instance
        
        
class VotePollForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Choice.objects.none(), widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)

        self.fields['choice'].queryset = question.choice_set.all()