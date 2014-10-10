#coding:utf-8
import uuid
import time
import os
import json
from django.shortcuts import render,render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login,logout
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.conf import settings

from PIL import Image

from account.emailhelper import send_confirmemail
from account.models import User,Register_Temp,UserFollow
from quest.models import Event,EventContent
from account.helper import follow_user as helper_follow_user,create_user
from quest.solrhelper import UserSolr
from redishelper.user import is_follow,get_user_by_id,update_avtar
from redishelper.timeline_util import get_events_list

@csrf_protect
def index(request):
    return render_to_response('login.html',context_instance=RequestContext(request))

def register_user(request):
    if request.method=='POST':
        try:
            name=request.POST['name']
            surname=request.POST['surname']
            email=request.POST['email']
            password=request.POST['password']
            activecode=unicode(uuid.uuid5(uuid.NAMESPACE_DNS,email.encode('utf-8')))
            user=User.objects.filter(email=email)
            if user and len(user)>0:
                return HttpResponse(json.dumps({"status":"fail","message":u"请使用其他邮箱注册".encode('utf-8')}))
            create_user(email=email,password=password,name=name,surname=surname,activecode=activecode)
            try:
                send_confirmemail(email,activecode,surname+name)
            except Exception,e:
                import pdb;pdb.set_trace()
                User.objects.filter(email=email).delete()
                Register_Temp.objects.filter(email=email).delete()
                return HttpResponse(json.dumps({"status":"fail","message":u"邮件发送失败".encode('utf-8')}))
            return HttpResponse(json.dumps({"status":"fail","message":u"注册成功".encode('utf-8')}))
        except Exception,e:
            return HttpResponse(json.dumps({"status":"fail","message":u"未知错误".encode('utf-8')}))

def login_user(request):
    try:
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            return HttpResponse(json.dumps({"status":"success"}))
        else:
            return  HttpResponse(json.dumps({"status":"fail","message":u"用户名或者密码错误".encode('utf-8')}))
    except Exception,e:
        returnHttpResponse(json.dumps({"status":"fail","message":u"异常".encode('utf-8')}))

def logout_user(request):
    try:
        logout(request)
        return HttpResponseRedirect("/account/?login")
    except Exception,e:
        return HttpResponse(u'异常')

def activate_user(request,activecode=None):
    try:
        info=Register_Temp.objects.filter(activecode=activecode)
        if activecode and info and len(info)>0:
            user=User.objects.get(email=info[0].email)
            user.is_active=True
            user.save()
            user=authenticate(email=info[0].email,auth_by_email=True)
            login(request,user)
            return HttpResponse(u'成功')
    except Exception,e:  
        return HttpResponse(u'失败')

@csrf_protect
def get_userinfo(request,userid):
    if not userid:
        userid=request.user.id;
        userinfo=request.user
    userinfo=get_user_by_id(userid)
    events=get_events_list(userid)
    is_self=False
    is_followed=is_follow(request.user.id,userid)
    if int(userid)==request.user.id:
        is_self=True
    return render_to_response("userinfo.html",{"events_list":events["event_list"],"statistics":events["statistics"],"userinfo":\
            userinfo,"is_self": is_self,"is_followed":is_followed},context_instance=RequestContext(request))

def follow_user(request): 
    try:
        if request.method=="POST":
            userid=request.POST.get("uid",None)
            ftype=request.POST.get('type',None)
            if userid and request.user.is_authenticated():
                touserid=get_user_by_id(userid)
                helper_follow_user(touserid,ftype,request.user)
        return HttpResponse("Ok")
    except Exception,e:
        return HttpResponse("error")

def upload_image(request):
    img=request.FILES.get("avat_file",None)
    if img:
        subdir="Image/"+time.strftime("%Y/%m/%d/",time.localtime())
        image_dir=settings.MEDIA_ROOT+subdir
        image_name=str(uuid.uuid1())+".jpg"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        f=open(image_dir+image_name,"wb")
        f.write(img.read())
        f.close()
        script="<script type='text/javascript' >parent.show_avatar({'src':'"+settings.MEDIA_URL+subdir+image_name+"'})</script>'"
        return HttpResponse(script)
    else:
        return HttpResponse("error")

@login_required
def change_image(request):
    img=request.FILES.get("avat_file",None)
    if img:
        subdir="Image/"+time.strftime("%Y/%m/%d/",time.localtime())
        image_dir=settings.MEDIA_ROOT+subdir
        image_name=str(uuid.uuid1())+".jpg"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        img=Image.open(img)
        img=img.resize((150,150),Image.ANTIALIAS)
        #f=open(image_dir+image_name,"wb")
        #f.write(img.read())
        #f.close()
        img.save(image_dir+image_name)
        user=request.user
        #user.avatar=settings.MEDIA_URL+subdir+image_name
        #user.avatar=img
        User.objects.filter(pk=user.id).update(avatar=settings.MEDIA_URL+subdir+image_name)
        update_avtar(user.id,settings.MEDIA_URL+subdir+image_name)
        script="<script type='text/javascript' >parent.show_avatar({'src':'"+settings.MEDIA_URL+subdir+image_name+"'})</script>'"
        return HttpResponse(script)
    else:
        return HttpResponse("error")

def get_suggestions(request):
    if request.method=="GET":
        q=request.GET.get('q','')
        solr=UserSolr()
        #import pdb;pdb.set_trace()
        docs=solr.suggestion(word=q)
        return HttpResponse(json.dumps(docs))
    else:
        return None

    

