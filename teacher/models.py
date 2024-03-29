from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=500)
    teacher = models.ForeignKey(User)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['start_date',]
    
    @models.permalink
    def get_absolute_url(self):
        return ('teacher:course_detail', (self.id,), {})
     
    def __unicode__(self):
        return self.name

class Test(models.Model):
    name = models.CharField(max_length=500)
    course = models.ForeignKey('Course')
    sent = models.DateTimeField(null=True, blank=True)
    expires = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField()

    class Meta:
        ordering = ("expires",)

    @models.permalink
    def get_absolute_url(self):
        return ('teacher:test_detail', (self.id,), {})

    def __unicode__(self):
        return self.name

class Question(models.Model):
    type = models.CharField(max_length=50, choices=(('multiple_choice', 'Multiple Choice'),
                                                     ('essay', 'Essay'), ('fill_blank', 'Fill Blank')))
    question = models.CharField(max_length=5000)
    test = models.ForeignKey('Test')
    ordering = models.IntegerField()

    class Meta:
        ordering = ['ordering',]

    @models.permalink
    def get_absolute_url(self):
        return ('teacher:update_question', (self.id,), {})

    def __unicode__(self):
        return self.question

class Answer(models.Model):
    answer = models.CharField(max_length=500)
    question = models.ForeignKey('Question')
    ordering = models.IntegerField()

    class Meta:
        ordering = ('ordering',)

    @models.permalink
    def get_absolute_url(self):
        return ('teacher:update_answer', (self.id,), {})

    def __unicode__(self):
        return self.answer
        
class MultipleChoiceAnswer(Answer):
    is_correct = models.BooleanField()
    
    @models.permalink
    def get_absolute_url(self):
        return ('teacher:update_multiplechoiceanswer', (self.id,), {})

class TakenTest(models.Model):
    user = models.ForeignKey(User)
    test = models.ForeignKey('Test')

    class Meta:
        ordering = ("test",)
        unique_together = ("user", "test")

    def __unicode__(self):
        return "%s %s" % (self.test, self.user)