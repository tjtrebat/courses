# Create your views here.

from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext as _

from courses.teacher.forms import *
from courses.registration.models import *

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def create_student(request, template='teacher/student_form.html'):
    if request.method == "POST":
        form = AddStudentForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            msg = _("The %(verbose_name)s was added successfully.") %\
                  {"verbose_name": User._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(reverse('teacher:course_list'))
    else:
        form = AddStudentForm(request.user)
    return render_to_response(template, {'form': form},
        context_instance=RequestContext(request))

@login_required
def update_student(request, student_id, template='teacher/student_form.html'):
    student_profile = get_object_or_404(request.user.profilesAsTeacher.all(), pk=student_id)
    student = student_profile.user
    if request.method == "POST":
        form = ChangeStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            msg = _("The %(verbose_name)s was updated successfully.") %\
                  {"verbose_name": User._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(reverse('teacher:course_list'))
    else:
        form = ChangeStudentForm(instance=student)
    return render_to_response(template, {'student': student,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def student_list(request, template='teacher/student_list.html'):
    students = []
    for user_profile in UserProfile.objects.filter(teacher=request.user):
        students.append(user_profile.user)
    return render_to_response(template, {'students': students},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def create_course(request, template='teacher/course_form.html'):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            msg = _("The %(verbose_name)s was added successfully.") %\
                  {"verbose_name": Course._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(reverse('teacher:course_list'))
    else:
        form = CourseForm()
    request.breadcrumbs(_("Add %(verbose_name)s") %\
                        {"verbose_name": Course._meta.verbose_name}, request.path_info)
    return render_to_response(template, {'form': form},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def course_list(request, template='teacher/course_list.html'):
    if request.method == "POST":
        form = CourseListForm(request.user, request.POST)
        if form.is_valid():
            template = 'teacher/courses_confirm_action.html'
            if request.POST.get("post", "") == "yes":
                selected_courses = form.cleaned_data['courses']
                for course_id in selected_courses:
                    course = get_object_or_404(Course, pk=course_id)
                    course.delete()
                msg = _("Successfully deleted %d %s.") %\
                      (len(selected_courses), Course._meta.verbose_name
                      if len(selected_courses) < 2 else Course._meta.verbose_name_plural)
                messages.success(request, msg, fail_silently=True)
                return HttpResponseRedirect(reverse("teacher:course_list"))
        else:
            messages.success(request, "No items have been changed.", fail_silently=True)
    else:
        form = CourseListForm(request.user)
    return render_to_response(template, {'form': form},
        context_instance=RequestContext(request))

@login_required
def course_detail(request, course_id, template='teacher/course_detail.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    if request.method == "POST":
        form = CourseDetailForm(request.user, request.POST)
        if form.is_valid():
            template = 'teacher/tests_confirm_action.html'
            if request.POST.get("post", "") == "yes":
                selected_tests = form.cleaned_data['tests']
                for test_id in selected_tests:
                    test = get_object_or_404(Test, pk=test_id)
                    test.delete()
                msg = _("Successfully deleted %d %s.") %\
                      (len(selected_tests), Test._meta.verbose_name
                      if len(selected_tests) < 2 else Test._meta.verbose_name_plural)
                messages.success(request, msg, fail_silently=True)
                return HttpResponseRedirect(reverse("teacher:course_detail", args=[course.pk]))
        else:
            messages.success(request, "No items have been changed.", fail_silently=True)
    else:
        form = CourseDetailForm(request.user)
    request.breadcrumbs(course.name, request.path_info)
    return render_to_response(template, {'form': form,
                                         'course': course},
        context_instance=RequestContext(request))

@login_required
def update_course(request, course_id, template='teacher/course_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save(request=request)
            msg = _("The %(verbose_name)s was updated successfully.") %\
                  {"verbose_name": Course._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(reverse('teacher:course_list'))
    else:
        form = CourseForm(instance=course)
    request.breadcrumbs(course.name, request.path_info)
    return render_to_response(template, {'course': course,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
def delete_course(request, course_id, template='teacher/course_confirm_delete.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    if request.method == 'POST':
        course.delete()
        msg = _("The %(verbose_name)s was deleted successfully.") %\
              {"verbose_name": Course._meta.verbose_name}
        messages.success(request, msg, fail_silently=True)
        return HttpResponseRedirect(reverse("teacher:course_list"))
    request.breadcrumbs(course.name, request.path_info)
    return render_to_response(template, {'course': course},
        context_instance=RequestContext(request))

@login_required
def create_test(request, course_id, template='teacher/test_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    if request.method == "POST":
        form = TestForm(course.pk, request.POST)
        if form.is_valid():
            form.save()
            msg = _("The %(verbose_name)s was added successfully.") %\
                  {"verbose_name": Test._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(reverse("teacher:create_question", args=[form.instance.pk]))
    else:
        form = TestForm(course.pk)
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (_("Add %(verbose_name)s") %\
         {"verbose_name": Test._meta.verbose_name}, request.path_info),
    ])
    return render_to_response(template, {'course': course,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
def test_detail(request, test_id, template='teacher/test_detail.html'):
    test = get_object_or_404(Test.objects.select_related(), pk=test_id)
    course = test.course
    if request.user != course.teacher: raise Http404
    QuestionFormSet = formset_factory(QuestionForm, extra=0)
    if request.method == "POST":
        formset = QuestionFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
    else:
        #initial_data = []
        #for i in range(6):
        #    initial_data.append({"test": test.pk, "ordering": i + 1})
        #formset = QuestionFormSet(initial=initial_data, prefix='questions')
        formset = QuestionFormSet(initial=[{"test": test.pk}] * 7)
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
    ])
    return render_to_response(template, {'formset': formset,
                                         'test': test},
        context_instance=RequestContext(request))

@login_required
def update_test(request, test_id, template='teacher/test_form.html'):
    test = get_object_or_404(Test.objects.select_related(), pk=test_id)
    course = test.course
    if request.user != course.teacher or test.is_sent: raise Http404
    if request.method == "POST":
        form = TestForm(course.pk, request.POST, instance=test)
        if form.is_valid():
            form.save()
            msg = _("The %(verbose_name)s was updated successfully.") %\
                  {"verbose_name": Test._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(course.get_absolute_url())
    else:
        form = TestForm(course.pk, instance=test)
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
def delete_test(request, test_id, template='teacher/test_confirm_delete.html'):
    test = get_object_or_404(Test.objects.select_related(), pk=test_id)
    course = test.course
    if request.user != course.teacher: raise Http404
    if request.method == 'POST':
        test.delete()
        msg = _("The %(verbose_name)s was deleted successfully.") %\
              {"verbose_name": Test._meta.verbose_name}
        messages.success(request, msg, fail_silently=True)
        return HttpResponseRedirect(course.get_absolute_url())
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test},
        context_instance=RequestContext(request))

@login_required
def send_test(request, test_id, template='teacher/test_confirm_send.html'):
    test = get_object_or_404(Test.objects.select_related(), pk=test_id)
    course = test.course
    if request.user != course.teacher: raise Http404
    if request.method == "POST":
        test.is_sent = True
        test.save()
        msg = _("The %(verbose_name)s was sent.") %\
              {"verbose_name": Test._meta.verbose_name}
        messages.success(request, msg, fail_silently=True)
        return HttpResponseRedirect(course.get_absolute_url())
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test},
        context_instance=RequestContext(request))

@login_required
def create_question(request, test_id, template='teacher/question_form.html'):
    test = get_object_or_404(Test.objects.select_related(), pk=test_id)
    course = test.course
    if request.user != course.teacher or test.is_sent: raise Http404
    if request.method == "POST":
        form = QuestionForm(test.pk, request.POST)
        if form.is_valid():
            form.save()
            msg = _("The %(verbose_name)s was added successfully.") %\
                  {"verbose_name": Question._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(test.get_absolute_url())
    else:
        form = QuestionForm(test.pk)
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (_("Add %(verbose_name)s") %\
         {"verbose_name": Question._meta.verbose_name}, request.path_info),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
def question_detail(request, question_id, template='teacher/question_detail.html'):
    question = get_object_or_404(Question.objects.select_related(), pk=question_id)
    test = question.test
    course = test.course
    if request.user != course.teacher: raise Http404
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question},
        context_instance=RequestContext(request))

@login_required
def update_question(request, question_id, template='teacher/question_form.html'):
    question = get_object_or_404(Question.objects.select_related(), pk=question_id)
    test = question.test
    course = test.course
    if request.user != course.teacher or test.is_sent: raise Http404
    if request.method == "POST":
        form = QuestionForm(test.pk, request.POST, instance=question)
        if form.is_valid():
            form.save()
            msg = _("The %(verbose_name)s was updated successfully.") %\
                  {"verbose_name": Question._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(test.get_absolute_url())
    else:
        form = QuestionForm(test.pk, instance=question)
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
def delete_question(request, question_id, template='teacher/question_confirm_delete.html'):
    question = get_object_or_404(Question.objects.select_related(), pk=question_id)
    test = question.test
    course = test.course
    if request.user != course.teacher or test.is_sent: raise Http404
    if request.method == 'POST':
        question.delete()
        msg = _("The %(verbose_name)s was deleted successfully.") %\
              {"verbose_name": Question._meta.verbose_name}
        messages.success(request, msg, fail_silently=True)
        return HttpResponseRedirect(test.get_absolute_url())
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question},
        context_instance=RequestContext(request))

@login_required
def create_answer(request, question_id, template='teacher/answer_form.html'):
    question = get_object_or_404(Question.objects.select_related(), pk=question_id)
    test = question.test
    course = test.course
    if request.user != course.teacher or test.is_sent: raise Http404
    if request.method == "POST":
        form = AnswerForm(question.pk, request.POST)
        if form.is_valid():
            form.save()
            msg = _("The %(verbose_name)s was added successfully.") %\
                  {"verbose_name": Answer._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = AnswerForm(question.pk)
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
        (_("Add %(verbose_name)s") %\
         {"verbose_name": Answer._meta.verbose_name}, request.path_info),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
def create_multiplechoiceanswer(request, question_id, template='teacher/multiplechoiceanswer_form.html'):
    question = get_object_or_404(Question.objects.select_related(), pk=question_id)
    test = question.test
    course = test.course
    if request.user != course.teacher or test.is_sent: raise Http404
    if request.method == "POST":
        form = MultipleChoiceAnswerForm(question.pk, request.POST)
        if form.is_valid():
            form.save()
            msg = _("The %(verbose_name)s was added successfully.") %\
                  {"verbose_name": Answer._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = MultipleChoiceAnswerForm(question.pk)
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
        (_("Add %(verbose_name)s") %\
         {"verbose_name": MultipleChoiceAnswer._meta.verbose_name}, request.path_info),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
def answer_detail(request, answer_id, template='teacher/answer_detail.html'):
    answer = get_object_or_404(Answer.objects.select_related(), pk=answer_id)
    question = answer.question
    test = question.test
    course = test.course
    if request.user != course.teacher: raise Http404
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
        (answer.answer, request.path_info),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'answer': answer},
        context_instance=RequestContext(request))

@login_required
def update_answer(request, answer_id, template='teacher/answer_form.html'):
    answer = get_object_or_404(Answer.objects.select_related(), pk=answer_id)
    question = answer.question
    test = question.test
    course = test.course
    if request.user != course.teacher or test.is_sent: raise Http404
    if request.method == "POST":
        form = AnswerForm(question.pk, request.POST, instance=answer)
        if form.is_valid():
            form.save()
            msg = _("The %(verbose_name)s was updated successfully.") %\
                  {"verbose_name": Answer._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = AnswerForm(question.pk, instance=answer)
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
        (answer.answer, request.path_info),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'answer': answer,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
def delete_answer(request, answer_id, template='teacher/answer_confirm_delete.html'):
    answer = get_object_or_404(Answer.objects.select_related(), pk=answer_id)
    question = answer.question
    test = question.test
    course = test.course
    if request.user != course.teacher or test.is_sent: raise Http404
    if request.method == 'POST':
        answer.delete()
        msg = _("The %(verbose_name)s was deleted successfully.") %\
              {"verbose_name": Answer._meta.verbose_name}
        messages.success(request, msg, fail_silently=True)
        return HttpResponseRedirect(question.get_absolute_url())
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
        (answer.answer, request.path_info),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'answer': answer},
        context_instance=RequestContext(request))

@login_required
def multiplechoiceanswer_detail(request, answer_id, template='teacher/multiplechoiceanswer_detail.html'):
    multiple_choice_answer = get_object_or_404(MultipleChoiceAnswer.objects.select_related(), answer_ptr=answer_id)
    question = multiple_choice_answer.question
    test = question.test
    course = test.course
    if request.user != course.teacher: raise Http404
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
        (multiple_choice_answer.answer, request.path_info),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'answer': multiple_choice_answer},
        context_instance=RequestContext(request))

@login_required
def update_multiplechoiceanswer(request, answer_id, template='teacher/multiplechoiceanswer_form.html'):
    answer = get_object_or_404(Answer.objects.select_related(), pk=answer_id)
    question = answer.question
    test = question.test
    course = test.course
    if request.user != course.teacher or test.is_sent: raise Http404
    multiple_choice_answer, created = MultipleChoiceAnswer.objects.get_or_create(answer_ptr=answer,
        question=question, answer=answer.answer, ordering=answer.ordering)
    if request.method == "POST":
        form = MultipleChoiceAnswerForm(question.pk, request.POST, instance=multiple_choice_answer)
        if form.is_valid():
            form.save()
            msg = _("The %(verbose_name)s was updated successfully.") %\
                  {"verbose_name": Answer._meta.verbose_name}
            messages.success(request, msg, fail_silently=True)
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = MultipleChoiceAnswerForm(question.pk, instance=multiple_choice_answer)
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
        (multiple_choice_answer.answer, request.path_info),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'answer': multiple_choice_answer,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
def delete_multiplechoiceanswer(request, answer_id, template='teacher/multiplechoiceanswer_confirm_delete.html'):
    multiple_choice_answer = get_object_or_404(MultipleChoiceAnswer.objects.select_related(), answer_ptr=answer_id)
    question = multiple_choice_answer.question
    test = question.test
    course = test.course
    if request.user != course.teacher or test.is_sent: raise Http404
    if request.method == 'POST':
        multiple_choice_answer.delete()
        msg = _("The %(verbose_name)s was deleted successfully.") %\
              {"verbose_name": Answer._meta.verbose_name}
        messages.success(request, msg, fail_silently=True)
        return HttpResponseRedirect(question.get_absolute_url())
    request.breadcrumbs([
        (course.name, course.get_absolute_url()),
        (test.name, test.get_absolute_url()),
        (question.question, question.get_absolute_url()),
        (multiple_choice_answer.answer, request.path_info),
    ])
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'answer': multiple_choice_answer},
        context_instance=RequestContext(request))

@login_required
def sort_question(request):
    if not request.is_ajax(): raise Http404
    for i, question_id in enumerate(request.POST.getlist("question[]")):
        question = get_object_or_404(Question.objects.select_related(), pk=question_id)
        if request.user == question.test.course.teacher:
            question.ordering = i + 1
            question.save()
    return HttpResponse()

@login_required
def sort_answer(request):
    if not request.is_ajax(): raise Http404
    for i, answer_id in enumerate(request.POST.getlist("answer[]")):
        answer = get_object_or_404(Answer.objects.select_related(), pk=answer_id)
        if request.user == answer.question.test.course.teacher:
            answer.ordering = i + 1
            answer.save()
    return HttpResponse()