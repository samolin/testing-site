from django.contrib import admin

from .models import Test, Question, Choice, Answer
from .forms import ChoiceAdminForm, ChoiceInlineFormset


class QuestionInline(admin.TabularInline):
    model = Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    formset = ChoiceInlineFormset


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        QuestionInline,
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'test']
    list_filter = ['test']
    inlines = [
        ChoiceInline,
    ]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'title', 'right_answer']
    list_filter = ['question']
    form = ChoiceAdminForm


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'choice']
    list_filter = ['question']
