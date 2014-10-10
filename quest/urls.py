#coding:utf-8
from django.conf.urls import patterns,url

urlpatterns=patterns('quest.views',
        url(r'^topic/add/$','add_topic'),
        url(r'^topic/get/$','query_topic'),
        url(r'^submittal/$','submit_question'),
        url(r'^hotquestions/$','get_hotquestion'),
        url(r'^(?P<question_id>\d+)[/]{0,1}$','show_question',name="question_detail"),
        url(r'^(?P<question_id>\d+)/answers$','get_answers'),
        url(r'^submittal/$','submit_question'),
        url(r'^answer/add$','add_answer'),
        url(r'^answer/vote$','vote_answer'),
        url(r'^comment/add$','add_comment'),
        url(r'^comment/get$','get_comment'),
        url(r'^follow/$','follow_question'),
        url(r'^image/$','image_test'),
        url(r'^image/upload/$','image_upload'),
        url(r'^m1/$','get_questions1'),
        url(r'searchsuggestions/$','get_suggestions'),
        url(r'search/$','search_results'),
        url(r'','main'),
        )
