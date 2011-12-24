__author__ = 'Tom'

from teacher.models import *
from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^courses/$', 'teacher.views.course_list', name='course_list'),
                       url(r'^course/(?P<course_id>\d+)/$', 'teacher.views.course_detail', name='course_detail'),
                       url(r'^course/(?P<course_id>\d+)/edit/$', 'teacher.views.update_course', name='update_course'),
                       url(r'^course/add/$', 'teacher.views.create_course', name='create_course'),
                       url(r'^course/(?P<course_id>\d+)/delete/$', 'teacher.views.delete_course', name='delete_course'),
                       url(r'^student/add/$', 'teacher.views.create_student', name='create_student'),
                       url(r'^student/(?P<student_id>\d+)/$', 'teacher.views.update_student', name='update_student'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/$', 'teacher.views.test_detail', name='test_detail'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/edit/$', 'teacher.views.update_test', name='update_test'),
                       url(r'^course/(?P<course_id>\d+)/test/add/$', 'teacher.views.create_test', name='create_test'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/delete/$', 'teacher.views.delete_test', name='delete_test'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/send/$', 'teacher.views.send_test', name='send_test'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/$', 'teacher.views.question_detail', name='question_detail'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/edit/$', 'teacher.views.update_question', name='update_question'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/add/$', 'teacher.views.create_question', name='create_question'),       
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/delete/$', 'teacher.views.delete_question', name='delete_question'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/sort/$', 'teacher.views.sort_question', name='sort_question'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/$', 'teacher.views.answer_detail', name='answer_detail'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/edit/$', 'teacher.views.update_answer', name='update_answer'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/answer/add/$', 'teacher.views.create_answer', name='create_answer'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/delete/$', 'teacher.views.delete_answer', name='delete_answer'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/answer/sort/$', 'teacher.views.sort_answer', name='sort_answer'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/multiple-choice-answer/(?P<answer_id>\d+)/$', 'teacher.views.multiplechoiceanswer_detail', name='multiplechoiceanswer_detail'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/multiple-choice-answer/(?P<answer_id>\d+)/edit/$', 'teacher.views.update_multiplechoiceanswer', name='update_multiplechoiceanswer'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/multiple-choice-answer/add/$', 'teacher.views.create_multiplechoiceanswer', name='create_multiplechoiceanswer'),
                       url(r'^course/(?P<course_id>\d+)/test/(?P<test_id>\d+)/question/(?P<question_id>\d+)/multiple-choice-answer/(?P<answer_id>\d+)/delete/$', 'teacher.views.delete_multiplechoiceanswer', name='delete_multiplechoiceanswer'),
)