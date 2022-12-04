from django.db import models


class Test(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')


    def __str__(self):
        return self.name


class Answer(models.Model):

    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test')
    question = models.CharField(max_length=100)
    answer_1 = models.CharField(max_length=300)
    answer_2 = models.CharField(max_length=300)
    answer_3 = models.CharField(max_length=300, blank=True, null=True)
    answer_4 = models.CharField(max_length=300, blank=True, null=True)
    answer_5 = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.question