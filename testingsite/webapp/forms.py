from django import forms
from django.core.exceptions import ValidationError
from .models import Answer, Choice


class AnswerForm(forms.Form):

    class Meta:
        model = Answer
        fields = ['choice']

    def __init__(self, *args, **kwargs):
        if 'question_id' in kwargs:
            question_id = kwargs.pop('question_id')
        else:
            question_id = 0
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.ChoiceField(
            required=True,
            choices=Choice.objects.values_list('title', 'title').filter(question_id=question_id), 
            widget=forms.RadioSelect(attrs={"class":"choices"}),
            error_messages={'required': 'Вы не выбрали ничего'}
        )


class ChoiceInlineFormset(forms.models.BaseInlineFormSet):

    def clean(self):
        various_choices = [form.cleaned_data.get('right_answer') for form in self.forms]
        if True not in various_choices:
            raise ValidationError('Хотя бы один ответ должен быть правильным')
        elif False not in various_choices:
            raise ValidationError('Все ответы не могут быть правильными')
        return self.cleaned_data
   