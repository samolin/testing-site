from django.db import models
from django.contrib.auth.models import User

class Test(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=4096)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test')

    def __str__(self):
           return self.title


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, related_name='choice')
    title = models.CharField(max_length=4096)
    right_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.choice.title