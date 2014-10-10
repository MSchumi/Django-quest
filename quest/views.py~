#coding:utf-8
import uuid
import os
import json
import time
from datetime import datetime

from django.shortcuts import render,render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template import loader

from PIL import Image

from quest.helper import *
from quest.models import Question,Topic,Answer,Comment,AnswerEvaluation,QustionFollow
from feed.models import Activity
from quest.signals import question_submit_done
from quest.solrhelper import QSolr,QuestionSolr,AnswerSolr,UserSolr
from redishelper.user import is_follow_question
from redishelper.question import (load_question_by_question,get_question_from_redis,get_answers_from_redis,get_answer_by_answer_id,)
from quest.redis_util import  add_answer_to_redis,add_comment_to_redis,add_question_to_redis,submit_vote_to_redis,cancel_vote_to_redis,follow_question_to_redis,\
        cancel_follow_question_to_redis
from redishelper.timeline_util import get_activities_list


def main(request):
    "主页面加载 如果用户登录并且有关注好友,则加载好友动态，否则加载回答数量最多的问题"
    if request.user.is_authenticated(): 
        activity_list=get_activities_list(request.user.id,0,15)
        if len(activity_list["activity_list"])>0:
            return render_to_response("main.html",activity_list,context_instance=RequestContext(request))
    question_list= Question.questionobjects.get_questions()
    return render_to_response("main.html",{"questions":question_list},context_instance=RequestContext(request))

def submit_question(request):
    try:
        if request.method=="POST":
            question=Question()
            title=request.POST["title"]
            content=request.POST["content"]
            category=request.POST["category"]
            user=request.user
            addtime=datetime.now()
            if content and title:
                question_id=add_question_to_redis(user=request.user,content=content,title=title,category=category,addtime=addtime)
                question=Question.questionobjects.create(id=question_id,user=request.user,content=content,title=title,category=category,addtime=addtime)
                return HttpResponse(str(question.id))
            else:
                return HttpResponse(u"内容不能为空")
    except Exception,e: 
        return HttpResponse(u'error')

@csrf_protect
def add_topic(request):
    try:
        if request.method=="POST":
            topic=Topic()
            topic.title=request.POST["title"]
            topic.addtime=date.today()
            topic.save()
            event_content={"id":topic.id,"title":topic.title}
            save_event(request.user.id,1,event_content,topic.id)
            return HttpResponse("添加完成")
    except Exception,e:
        print e

def query_topic(request):
    try:
        if request.method=="GET" and request.GET["q"]!=" ":
            topic_str=""
            topic_set=Topic.objects.filter(title__contains=request.GET["q"])
            if topic_set and len(topic_set)>0:
                for topic in topic_set:
                    topic_str+="\""+topic.title+"\","
                topic_str="["+topic_str[:-1]+"]"
                return HttpResponse(topic_str)
            else:
                return HttpResponse("[]")
        else:
            return HttpResponse("[]")
    except Exception ,e:
        print e

def get_hotquestion(request):
    try:
        if request.method=="GET":
            start=request.GET["start"]
            end=request.GET["end"]
            question_set=Question.objects.all()[start:end]
            q_str=""
            for question in question_set:
                q_str+="{\"title\":\""+question.title+"\",\"content\":\""+question.content.replace("\"","#")+"\"},"
            q_str="{\"items\":["+q_str[:-1]+"]}"
            return HttpResponse(q_str)
        else:
            return HttpResponse("{\"itens\":[]}")
    except Exception,e:
        print e

def get_questions1(request):
    try:
        if request.method=="GET": 
            question_list= Question.questionobjects.get_questions()
            #import pdb;pdb.set_trace()
            html_str=render_to_string("question_list.html",{"questions":question_list})
            return HttpResponse(html_str)
        else:
            return HttpResponse("22")
    except Exception,e:
        return None 

def show_question(request,question_id):
    question=None
    answers=None
    if request.user.is_authenticated():
        user_id=request.user.pk
        question=get_question_from_redis(question_id)
        question.followed=is_follow_question(question_id,user_id)
        answers=get_answers_from_redis(question_id,user_id=user_id)
    else:
        question=get_question_from_redis(question_id)
        answers=get_answers_from_redis(question_id)
    if not question:
        raise Http404
    load_question_by_question(question)
    return render_to_response("question.html",{"question":question,"answers_list":answers},context_instance=RequestContext(request))
def get_question_info_by_id(request,question_id):
    question=Question.objects.filter(pk=question_id)

def add_answer(request):
    question_id=request.POST["questionid"]
    content=request.POST["content"]
    addtime=datetime.now()
    answer_id=add_answer_to_redis(user=request.user,addtime=addtime,question_id=question_id,content=content)
    question=get_question_from_redis(question_id)
    answer=Answer.answerobjects.create(answer_id,addtime=addtime,user=request.user,question=question,content=content);
    html_str=render_to_string('answerlist.html',{'answers_list':[answer]})
    return HttpResponse(html_str)

def get_answers_htmlstr(request,question_id):
    answers=Answer.answerobjects.get_answerlist(question_id,request.user.id)
    html_str=render_to_string('answerlist.html',{'answers_list':answers})
    return html_str

def get_answers(request,question_id):
    html_str=get_anwers_htmlstr(question_id)
    return HttpResponse(html_str)

def get_comment(request):
    "获取评论列表 加载更多尚未细化"
    answer_id=request.GET["answerid"]
    comments=Comment.objects.select_related('user','touser').filter(answer_id=answer_id)
    html_str=render_to_string("commentlist.html",{"comments_list":comments},context_instance=RequestContext(request))
    return HttpResponse(html_str)

def add_comment(request):
    "添加评论"
    if request.method=="POST":
        answer_id=request.POST.get("answerid",None)
        question_id=request.POST.get("questionid",None)
        content=request.POST.get("content",None)
        touser_id=int(request.POST.get("touser",request.user.id))
        answer=get_answer_by_answer_id(int(answer_id))
        if answer_id and content and touser_id:
            addtime=datetime.now()
            comment_id=add_comment_to_redis(answer_id=answer_id,addtime=addtime,content=content,user=request.user,touser_id=touser_id)
            comment=Comment.commentobjects.create(id=comment_id,answer=answer,addtime=addtime,content=content,user=request.user,touser_id=touser_id)
            html_str=render_to_string("commentlist.html",{"comments_list":[comment]},context_instance=RequestContext(request))
            return HttpResponse(html_str)
    return HttpResponse("error")

@login_required
def vote_answer(request):
    "用户对问题投票+表示新增-表示update 用户字投票问题尚未解决"
    answer_id=request.POST["answerid"]
    op_type=request.POST.get("type","+")
    status=int(request.POST["status"])
    evaluation_id=request.POST.get("evaluation_id",None)
    answer=get_answer_by_answer_id(int(answer_id))
    if answer.user.id!=request.user.id:
        if op_type!="+":
            cancel_vote_to_redis(user=request.user,answer_id=answer,status=status,evaluation_id=evaluation_id)
            AnswerEvaluation.evaluationobjects.cancel_vote(user=request.user,answer=answer,status=status,evaluation_id=evaluation_id)
        else:
            submit_vote_to_redis(user=request.user,answer_id=answer_id,status=status,evaluation_id=evaluation_id)
            evaluation_id=AnswerEvaluation.evaluationobjects.submit_voter(user=request.user,answer=answer,status=status,evaluation_id=evaluation_id)
            return  HttpResponse("{\"evaluation_id\":\""+str(evaluation_id)+"\"}")
        return HttpResponse("{\"status\":\"ok\"}")
    else:
        return HttpResponse("")
    
@csrf_protect
def image_test(request):
    return render_to_response("image.html",context_instance=RequestContext(request))

def image_upload(request):
    "图片上传测试 现在废弃"
    reqfile = request.FILES['file1']
    img = Image.open(reqfile)
    img.thumbnail((500,500),Image.ANTIALIAS)
    if not os.path.exists("image"):
        os.mkdir("image")
    img.save("F:/F1/Question/image/c1.jpg")
    return HttpResponse("ok"+os.path.abspath("image"))

def follow_question(request):
    "关注问题"
    if request.method=="POST":
        qid=request.POST.get("qid",None)
        typecode=request.POST.get("type",None)
        question=get_question_from_redis(int(qid))
        if qid and typecode:
            if typecode=="0":
                follow=QustionFollow(question=question,user=request.user)
                follow.follow_question(request.user)
                follow_question_to_redis(qid,request.user.id)
            else:
                follow=QustionFollow.objects.filter(question=question,user=request.user)[0]
                follow.cancel_follow(request.user)
                cancel_follow_question_to_redis(qid,request.user.id)
            return HttpResponse()
        else:
            return Http404

def server_error(request,template_name="404.html"):
    "定义404页面"
    return render_to_response(template_name,context_instance=RequestContext(request))

def get_suggestions(request):
    "获取问题提示"
    if request.method=="GET":
        q=request.GET.get('q','')
        solr=QuestionSolr()
        docs=solr.suggestion(word=q)
        return HttpResponse(json.dumps(docs))
    else:
        return None

def search_results(request):
    "检索结果默认检索问题"
    if request.method=='GET':
        q=request.GET.get('q','')
        searchtype=request.GET.get('type','question')
        if searchtype=="user":
            solr=UserSolr()
        elif searchtype=="answer":
            solr=AnswerSolr()
        else:
            solr=QuestionSolr()
        data=solr.search_by_keyword(q)
        return render_to_response('search.html',{'searchword':q,'searchtype':searchtype,'data':data})
    return HttpResponse()





