from django.shortcuts import render, redirect, get_list_or_404
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Test, Question, Choice, Answer
from .forms import AnswerForm

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


class TestListView(ListView):
    model = Test
    template_name = 'home.html'


@login_required
def answer_home(request, test_name=None):
    questions = get_list_or_404(Test.objects.get(slug=test_name).test.all())
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    question_id = page.object_list[0].id
    form = AnswerForm(question_id=question_id)
    test_url = page.object_list[0].test.slug
    context = {
        'page': page, 
        'form': form, 
        'test_url': test_url,
        'amount_pages': paginator.num_pages,
    }
    if request.method == 'POST':
        print('request_post: ', request.POST)
        question = Question.objects.get(title=request.POST['question'])
        form = AnswerForm({'choice':request.POST.get('choice'), 'question_id':question_id})
        form.fields['choice'].choices = [(request.POST.get('choice'), request.POST.get('choice'),)]
        if form.is_valid():
            choice = form.cleaned_data['choice']
            print("cleaned_data: ", form.cleaned_data)
            try:
                answer = Answer.objects.get(user=request.user, question=question)
                answer.choice=Choice.objects.filter(question=question).get(title=choice)
            except:
                answer = Answer(
                    user=request.user,
                    question=question,
                    choice=Choice.objects.filter(question=question).get(title=choice),
                )
            answer.save()
            print('Form is saved')
            if page.has_next() == True:
                return redirect(f'/{test_name}/?page={page.next_page_number()}')
            return redirect(f'/{test_name}/result')
        else:
            print('We are in validation error')
            form_errors = form.errors['choice'].as_text().replace('*', '')
            form = AnswerForm(question_id=question_id)
            context['form_errors'] = form_errors
            return render(request, 'question.html', context) 
    return render(request, 'question.html', context) 


@login_required
def result(request, test_name=None):
    test_id = Test.objects.filter(slug=test_name).first().id
    result = Answer.objects.filter(user=request.user, question__test=test_id).all()
    statistic = amount_of_right_answers(result)
    rights = statistic.get('rights')
    wrongs = statistic.get('wrongs')
    percent = round(statistic.get('percent'), 2)
    context = {
        "user": request.user, 
        "result": result,
        "rights": rights,
        "wrongs": wrongs,
        "percent": percent,
    }
    return render(request, 'result.html', context)


def amount_of_right_answers(result):
    amount = 0
    rights = 0
    for answer in result:
        amount += 1
        if answer.choice.right_answer:
            rights += 1
    wrongs = amount - rights
    percent = rights / amount * 100
    return { "rights": rights, "wrongs":wrongs, "percent": percent}
