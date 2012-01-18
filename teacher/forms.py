__author__ = 'Tom'

from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import *
from django.db.models import Max

from courses.teacher.models import *

class CourseListForm(forms.Form):
    def __init__(self, teacher, *args, **kwargs):
        super(CourseListForm, self).__init__(*args, **kwargs)
        self.fields['action'] = forms.CharField(max_length=150, widget=forms.Select(choices=(
            ("", "---------",),
            ("delete-selected", "Delete selected courses",),
            )))
        self.fields['courses'] = CoursesField(teacher, widget=forms.CheckboxSelectMultiple())

class AddStudentForm(UserCreationForm):
    def __init__(self, teacher, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.fields['courses'] = CoursesField(teacher)
       
    def save(self, commit=True, *args, **kwargs):
        student = super(AddStudentForm, self).save(commit=False, *args, **kwargs)
        if commit:
           student.save()
           student.groups.add(Group.objects.get(name="students"))
           profile = student.get_profile()
           profile.teacher = self.fields['courses'].teacher
           profile.save()
           for course in self.cleaned_data['courses']:
               profile.courses.add(course)
        return student

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ChangeStudentForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangeStudentForm, self).__init__(*args, **kwargs)
        self.profile = self.instance.get_profile()
        self.fields['courses'] = CoursesField(self.profile.teacher,
                                              initial=[course.pk for course in self.profile.courses.all()])

    def save(self, commit=True, *args, **kwargs):
        student = super(ChangeStudentForm, self).save(commit=False, *args, **kwargs)
        if commit:
           student.save()
           self.profile.courses.clear()
           for course in self.cleaned_data['courses']:
               self.profile.courses.add(course)
        return student

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class CoursesField(forms.MultipleChoiceField):
    def __init__(self, teacher, *args, **kwargs):
        super(CoursesField, self).__init__(*args, **kwargs)
        self.teacher = teacher
        self.required = False
        self.choices = ((course.pk, course.name) for course in self.teacher.course_set.all())

    def clean(self, value):
        for course_id in value:
            try:
                course = Course.objects.get(pk=course_id)
            except Course.DoesNotExist:
                raise forms.ValidationError('Course does not exist')
            else:
                if course not in self.teacher.course_set.all():
                    raise forms.ValidationError('Course does not exist')
        return value

class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = FormattedDateTimeField(required=False)
        self.fields['end_date'] = FormattedDateTimeField(required=False)

    def save(self, commit=True, request=None, *args, **kwargs):
        course = super(CourseForm, self).save(commit=False, *args, **kwargs)
        if commit:
            if request:
                course.teacher = request.user
            course.save()
        return course

    class Meta:
        model = Course
        exclude = ('teacher',)

class TestForm(forms.ModelForm):
    def __init__(self, course_id, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['course'].initial = course_id
        self.fields['course'].widget = forms.HiddenInput()
        self.fields['expires'] = FormattedDateTimeField(required=False)

    class Meta:
        model = Test
        exclude = ('sent', 'is_sent',)

class FormattedDateTimeField(forms.DateTimeField):
    widget = forms.DateTimeInput(format="%m/%d/%Y %I%M %p")

    def __init__(self, *args, **kwargs):
        super(FormattedDateTimeField, self).__init__(*args, **kwargs)
        self.input_formats = ('%m/%d/%Y %I:%M %p',)

class QuestionForm(forms.ModelForm):
    def __init__(self, test_id, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['test'].initial = test_id
        self.fields['test'].widget = forms.HiddenInput()
        self.fields['ordering'] = OrderedField(Question.objects.filter(test=test_id))

    class Meta:
        model = Question

class AnswerForm(forms.ModelForm):
    def __init__(self, question_id, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['question'].initial = question_id
        self.fields['question'].widget = forms.HiddenInput()
        self.fields['ordering'] = OrderedField(Answer.objects.filter(question=question_id))

    class Meta:
        model = Answer

class MultipleChoiceAnswerForm(AnswerForm):
    def __init__(self, question_id, *args, **kwargs):
        super(MultipleChoiceAnswerForm, self).__init__(question_id, *args, **kwargs)

    class Meta:
        model = MultipleChoiceAnswer

class OrderedField(forms.IntegerField):
    def __init__(self, queryset, *args, **kwargs):
        super(OrderedField, self).__init__(*args, **kwargs)
        self.initial = (queryset.aggregate(Max('ordering'))['ordering__max'] or 0) + 1
        self.widget = forms.HiddenInput()

    def clean(self, value):
        return super(OrderedField, self).clean(value)