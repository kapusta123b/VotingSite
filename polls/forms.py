from polls.models import Questions
from django import forms


class CreatePollForm(forms.ModelForm):

    class Meta:
        model = Questions
        fields = ['category', 'question_text']