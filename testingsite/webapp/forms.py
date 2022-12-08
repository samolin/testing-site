from django import forms
from django.core.exceptions import ValidationError
from .models import Answer, Choice


class AnswerForm(forms.Form):

    class Meta:
        model = Answer
        fields = ['choice']

    def __init__(self, *args, **kwargs):
        print('kwargs', kwargs)
        if 'question_id' in kwargs:
            print(kwargs)
            question_id = kwargs.pop('question_id')
        else:
            question_id = 0
        print('kwargs2', kwargs)
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.ChoiceField(
            required=True,
            choices=Choice.objects.values_list('title', 'title').filter(question_id=question_id), 
            widget=forms.CheckboxSelectMultiple(attrs={"class":"choices"}),
            error_messages={'required': 'Вы не выбрали ничего'}
        )


class ChoiceAdminForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ChoiceAdminForm, self).clean()
        if cleaned_data.get('right_answer') == False:
            if Choice.objects.filter(question = cleaned_data.get('question')).filter(right_answer = True).first() == None:
                raise ValidationError('Хотя бы один ответ должен быть правильным')
        return self.cleaned_data


class ChoiceInlineFormset(forms.models.BaseInlineFormSet):

    def clean(self):
        various_choices = [form.cleaned_data.get('right_answer') for form in self.forms]
        if True not in various_choices:
                raise ValidationError('Хотя бы один ответ должен быть правильным')
        return self.cleaned_data
        