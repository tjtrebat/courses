__author__ = 'Tom'

from teacher.models import *
from django.contrib import admin

class QuestionAdmin(admin.ModelAdmin):
    list_filter = ("test",)

class AnswerAdmin(admin.ModelAdmin):
    list_filter = ("question",)

admin.site.register(Course)
admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(TakenTest)