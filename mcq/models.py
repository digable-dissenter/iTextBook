from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

from book.models import Subtopic


class Question(models.Model):
    question = models.TextField()
    subtopic = models.ForeignKey(Subtopic)

    def __unicode__(self):
        return self.question


class QuestionForm(ModelForm):
    def __init__(self, *args, **kw):
        super(ModelForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'subtopic',
            'question', ]

    class Meta:
        model = Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question"]
    search_fields = ["question"]


admin.site.register(Question, QuestionAdmin)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=50)
    correct = models.BooleanField(default=False)

    def is_correct(self):
        return self.correct

    def __unicode__(self):
        return self.answer


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ('question',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["question", "answer", "correct"]

    search_fields = ["question", "answer"]


admin.site.register(Answer, AnswerAdmin)


class MCQGuess(models.Model):
    question = models.ForeignKey(Question)
    submitted_by = models.ForeignKey(User)
    answer_given = models.ForeignKey(Answer)
    guess_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(max_length=2, blank=False, null=False)


class MCQGuessForm(ModelForm):
    class Meta:
        model = MCQGuess


class MCQGuessAdmin(admin.ModelAdmin):
    list_display = ["submitted_by", "answer_given"]


admin.site.register(MCQGuess, MCQGuessAdmin)
