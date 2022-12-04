from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator

from .models import Test, Answer


def index(request):
    return render(request, 'home.html')


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


class TestListView(ListView):
    model = Test
    template_name = 'home.html'


class AnswerDetailView(DetailView):
    model = Answer
    template_name = 'question.html'


def answer_home(request, test_name=None):
    questions = Test.objects.get(slug=test_name).test.all()
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    args = {'questions': questions, 'page': page}
    return render(request, 'question.html', args) 