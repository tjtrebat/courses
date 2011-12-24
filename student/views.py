#__author__ = 'Tom'

from django.template import RequestContext
from django.shortcuts import render_to_response
from teacher.models import Test, TakenTest

def test_list(request, template='student/test_list.html'):
    tests = []
    taken_tests = []
    for course in request.user.get_profile().courses.all():
        for test in course.test_set.all():
            if TakenTest.objects.filter(user=request.user, test=test).count():
                taken_tests.append(test)
            elif test.is_sent():
                tests.append(test)
    return render_to_response(template, {'tests': tests, 'taken_tests': taken_tests},
                              context_instance=RequestContext(request))