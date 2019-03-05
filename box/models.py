from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from book.models import Subtopic


# Create your models here.

class Question(models.Model):
    subtopic = models.ForeignKey(Subtopic)
    text = models.TextField(max_length=500, blank=False, null=True)

    def __unicode__(self):
        return self.text


class QuestionForm(ModelForm):
    class Meta:
        model = Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["subtopic", "text"]

    list_filter = ["subtopic", "text"]


admin.site.register(Question, QuestionAdmin)


class Keyword(models.Model):
    question = models.ForeignKey(Question)
    text = models.TextField(max_length=50, blank=False, null=True)
    min_use = models.IntegerField(max_length=2, blank=False, null=False)

    def __unicode__(self):
        return self.text


class KeywordForm(ModelForm):
    class Meta:
        model = Keyword
        exclude = ('question',)


class KeywordAdmin(admin.ModelAdmin):
    list_display = ["text"]
    list_filter = ["text"]


admin.site.register(Keyword, KeywordAdmin)


class TestCase(models.Model):
    question = models.ForeignKey(Question)
    test_input = models.CharField(max_length=60, blank=False, null=True)
    test_output = models.CharField(max_length=60, blank=False, null=True)

    def __unicode__(self):
        return self.question.text


class TestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        exclude = ('question',)


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ["test_input", "test_output"]
    list_filter = ["test_input", "test_output"]


admin.site.register(TestCase, TestCaseAdmin)


class Attempt(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    score = models.CharField(max_length=60, blank=False, null=True)
    code = models.CharField(max_length=60, blank=False, null=True)
    feedback = models.TextField(max_length=500, blank=False, null=True)


class AttemptForm(ModelForm):
    class Meta:
        model = Attempt


class AttemptAdmin(admin.ModelAdmin):
    list_display = ["user", "question", "score", "code"]
    list_filter = ["user", "question", "score", "code"]


admin.site.register(Attempt, AttemptAdmin)
