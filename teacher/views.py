# Create your views here.

from django.shortcuts import *
from django.template import *
from django.http import *
from django.contrib import messages
from django.contrib.auth.models import *
from django.contrib.auth.decorators import *
from django.views.generic import create_update
from django.utils.translation import ugettext
from teacher.forms import *
from teacher.models import *
from registration.models import *

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def course_list(request, template='teacher/course_list.html'):
    courses = Course.objects.filter(teacher=request.user)
    students = []
    for user_profile in UserProfile.objects.filter(teacher=request.user):
        students.append(user_profile.user)
    return render_to_response(template, {'courses': courses,
                                         'students': students},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def course_detail(request, course_id, template='teacher/course_detail.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    return render_to_response(template, {'course': course},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def update_course(request, course_id, template='teacher/course_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save(request=request)
            return HttpResponseRedirect(course.get_absolute_url())
    else:
        form = CourseForm(instance=course)
    return render_to_response(template, {'course': course,
                                         'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def create_course(request, template='teacher/course_form.html'):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = CourseForm()
    return render_to_response(template, {'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def delete_course(request, course_id):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    redirect_to = "/courses/"
    return create_update.delete_object(request, Course, redirect_to, course_id)

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def update_student(request, student_id, template='teacher/student_form.html'):
    student_profile = get_object_or_404(UserProfile.objects.filter(teacher=request.user), pk=student_id)
    student = student_profile.user
    if request.method == "POST":
        form = ChangeStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/courses/")
    else:
        form = ChangeStudentForm(instance=student)  
    return render_to_response(template, {'student': student,
                                         'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def create_student(request, template='teacher/student_form.html'):
    if request.method == "POST":
        form = AddStudentForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/courses/")
    else:
        form = AddStudentForm(request.user)    
    return render_to_response(template, {'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def test_detail(request, course_id, test_id, template='teacher/test_detail.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    return render_to_response(template, {'course': course,
                                         'test': test},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def update_test(request, course_id, test_id, template='teacher/test_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    if not test.is_sent:
        if request.method == "POST":
            form = TestForm(course.pk, request.POST, instance=test)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(test.get_absolute_url())
        else:
            form = TestForm(course.pk, instance=test)
    else:
        raise Http404       
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def create_test(request, course_id, template='teacher/test_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    if request.method == "POST":
        form = TestForm(course.pk, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = TestForm(course.pk)
    return render_to_response(template, {'course': course,
                                         'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def delete_test(request, course_id, test_id):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    redirect_to = "/course/%s/" % course.pk
    return create_update.delete_object(request, Test, redirect_to, test_id,
                                       extra_context={'course': course})

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def send_test(request, course_id, test_id, template='teacher/test_confirm_send.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    if request.method == "POST":
        test.is_sent = True
        test.save()
        msg = ugettext("The %(verbose_name)s was sent.") %\
              {"verbose_name": Test._meta.verbose_name}
        messages.success(request, msg, fail_silently=True)
        return HttpResponseRedirect(test.get_absolute_url())
    return render_to_response(template, {'course': course,
                                         'test': test},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def question_detail(request, course_id, test_id, question_id, template='teacher/question_detail.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question
                                         },
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def update_question(request, course_id, test_id, question_id, template='teacher/question_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    if not test.is_sent:
        if request.method == "POST":
            form = QuestionForm(test.pk, request.POST, instance=question)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(question.get_absolute_url())
        else:
            form = QuestionForm(test.pk, instance=question)
    else:
        raise Http404
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def create_question(request, course_id, test_id, template='teacher/question_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    if not test.is_sent:
        if request.method == "POST":
            form = QuestionForm(test.pk, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(form.instance.get_absolute_url())
        else:
            form = QuestionForm(test.pk)    
    else:
        raise Http404
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'form': form},
        context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def delete_question(request, course_id, test_id, question_id):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    redirect_to = test.get_absolute_url()
    if test.is_sent:
        raise Http404
    return create_update.delete_object(request, Question, redirect_to, question_id,
                                       extra_context={'course': course,
                                                      'test': test})

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def answer_detail(request, course_id, test_id, question_id, answer_id, template='teacher/answer_detail.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    answer = get_object_or_404(question.answer_set.all(), pk=answer_id)
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'answer': answer},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def update_answer(request, course_id, test_id, question_id, answer_id, template='teacher/answer_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    answer = get_object_or_404(question.answer_set.all(), pk=answer_id)
    if not test.is_sent:
        if request.method == "POST":
            form = AnswerForm(question.pk, request.POST, instance=answer)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(answer.get_absolute_url())
        else:
            form = AnswerForm(question.pk, instance=answer)
    else:
        raise Http404
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'answer': answer,
                                         'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def create_answer(request, course_id, test_id, question_id, template='teacher/answer_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    if not test.is_sent:
        if request.method == "POST":
            form = AnswerForm(question.pk, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(form.instance.get_absolute_url())
        else:
            form = AnswerForm(question.pk)      
    else:
        raise Http404
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def delete_answer(request, course_id, test_id, question_id, answer_id):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    answer = get_object_or_404(question.answer_set.all(), pk=answer_id)
    redirect_to = question.get_absolute_url()
    if test.is_sent:
        raise Http404
    return create_update.delete_object(request, Answer, redirect_to, answer_id,
                                       extra_context={'course': course,
                                                      'test': test,
                                                      'question': question})

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def multiplechoiceanswer_detail(request, course_id, test_id, question_id, answer_id,
                                  template='teacher/multiplechoiceanswer_detail.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    multiple_choice_answer = get_object_or_404(MultipleChoiceAnswer, answer_ptr=answer_id)
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'answer': multiple_choice_answer},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def update_multiplechoiceanswer(request, course_id, test_id, question_id, answer_id,
                                  template='teacher/multiplechoiceanswer_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    answer = get_object_or_404(question.answer_set.all(), pk=answer_id)
    if not test.is_sent:
        multiple_choice_answer, created = MultipleChoiceAnswer.objects.get_or_create(answer_ptr=answer,
            question=question, answer=answer.answer, ordering=answer.ordering)
        if request.method == "POST":
            form = MultipleChoiceAnswerForm(question.pk, request.POST, instance=multiple_choice_answer)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(multiple_choice_answer.get_absolute_url())
        else:
            form = MultipleChoiceAnswerForm(question.pk, instance=multiple_choice_answer)
    else:
        raise Http404
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'answer': multiple_choice_answer,
                                         'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def create_multiplechoiceanswer(request, course_id, test_id, question_id,
                                  template='teacher/multiplechoiceanswer_form.html'):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    if not test.is_sent:
        if request.method == "POST":
            form = MultipleChoiceAnswerForm(question.pk, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(form.instance.get_absolute_url())
        else:
            form = MultipleChoiceAnswerForm(question.pk)
    else:
        raise Http404
    return render_to_response(template, {'course': course,
                                         'test': test,
                                         'question': question,
                                         'form': form},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def delete_multiplechoiceanswer(request, course_id, test_id, question_id, answer_id):
    course = get_object_or_404(request.user.course_set.all(), pk=course_id)
    test = get_object_or_404(course.test_set.all(), pk=test_id)
    question = get_object_or_404(test.question_set.all(), pk=question_id)
    answer = get_object_or_404(question.answer_set.all(), pk=answer_id)
    multiple_choice_answer = get_object_or_404(MultipleChoiceAnswer, answer_ptr=answer_id)
    redirect_to = question.get_absolute_url()
    if test.is_sent:
        raise Http404
    return create_update.delete_object(request, MultipleChoiceAnswer, redirect_to, answer_id,
                                       extra_context={'course': course,
                                                      'test': test,
                                                      'question': question})

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def sort_question(request, course_id, test_id):
    if request.is_ajax():
        for i, pk in enumerate(request.POST.getlist("question[]")):
            course = get_object_or_404(request.user.course_set.all(), pk=course_id)
            test = get_object_or_404(course.test_set.all(), pk=test_id)
            obj = get_object_or_404(test.question_set.all(), pk=pk)
            obj.ordering = i + 1
            obj.save()
    return HttpResponse()

@login_required
@user_passes_test(lambda u: u.get_profile().is_teacher())
def sort_answer(request, course_id, test_id, question_id):
    if request.is_ajax():
        for i, pk in enumerate(request.POST.getlist("answer[]")):
            course = get_object_or_404(request.user.course_set.all(), pk=course_id)
            test = get_object_or_404(course.test_set.all(), pk=test_id)
            question = get_object_or_404(test.question_set.all(), pk=question_id)
            obj = get_object_or_404(question.answer_set.all(), pk=pk)
            obj.ordering = i + 1
            obj.save()
    return HttpResponse()