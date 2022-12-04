from django.contrib import admin

from .models import Test, Answer

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'test_id', 'question', 'answer_1', 'answer_2', \
        'answer_3', 'answer_4', 'answer_5']
