#coding=utf-8

import redis
import json
from celery.task import task

from notification.models import Message
from quest.models import Event,QustionFollow
from feed.models import Activity
from redishelper.util import connect,get_next_event_id,get_next_activity_id,get_next_message_id
from redishelper.question_util import get_question_follower
from redishelper.redisconfig import *

def require_timeline(user_id):
    if not timeline_client.exists(USER_TIME_LINE_PREFIX+str(user_id)):
        timeline_client.lpush(-1)

def add_to_activity_timeline(user_id,activity_type,content_id,addtime,fuser_id,lpush=True):
    activity_info_id="t:"+str(activity_type)+"c:"+str(content_id)
    if lpush:
        timeline_client.lpush(USER_ACTIVITY_TIME_LINE_PREFIX+str(user_id),"u:"+str(fuser_id)+activity_info_id)
    else:
        timeline_client.rpush(USER_ACTIVITY_TIME_LINE_PREFIX+str(user_id),"u:"+str(fuser_id)+activity_info_id)
    timeline_client.hmset(USER_ACTIVITY_PREFIX+"u:"+str(user_id)+activity_info_id,{"activity_type":activity_type,"content_id":content_id,"addtime":\
            addtime.strftime(TIME_STRF),"fuser":fuser_id})
    #if is_push:
       #task_id=push_activity.delay(user_id,activity_type,content_id,addtime)

def add_to_event_timeline(user_id,activity_type,content_id,addtime,event_id,add=True,update=False,lpush=True):
    "添加个人动态"
    event_info_id="t:"+str(activity_type)+"c:"+str(content_id)
    if add:
        if update:
            timeline_client.lrem(USER_EVENT_TIME_LINE_PREFIX+str(user_id),0,event_info_id) 
            timeline_client.hmset(USER_EVENT_PREFIX+"u:"+str(user_id)+event_info_id,{"addtime":addtime.strftime(TIME_STRF)})
        else:
            #timeline_client.lpush(USER_EVENT_TIME_LINE_PREFIX+str(user_id),event_info_id)
            timeline_client.hmset(USER_EVENT_PREFIX+"u:"+str(user_id)+event_info_id,{"id":event_id,"activity_type":activity_type,"content_id":content_id,"addtime":\
                    addtime.strftime(TIME_STRF)})
        if lpush:
            timeline_client.lpush(USER_EVENT_TIME_LINE_PREFIX+str(user_id),event_info_id)
        else:
            timeline_client.rpush(USER_EVENT_TIME_LINE_PREFIX+str(user_id),event_info_id)
    else:
        timeline_client.lrem(USER_EVENT_TIME_LINE_PREFIX+str(user_id),0,event_info_id)
        timeline_client.delete(USER_EVENT_PREFIX+"u:"+str(user_id)+event_info_id)

def add_to_message_timeline(message_type,contentid,content,from_user_id,touser_id,addtime,only_all=False,status=1,lpush=True):
    message_info_id="t:"+str(message_type)+"c:"+str(contentid)
    taddtime=addtime
    addtime=addtime.strftime(TIME_STRF)
    if message_type==1:
        question_id=content["question_id"]
        question_follow=get_question_follower(question_id)
        question_follow.add(int(content["question_user_id"]))
        for user_id in question_follow:
            if int(user_id)!=int(from_user_id):
                if not lpush:
                     timeline_client.rpush(USER_MESSAGE_TIME_LINE_PREFIX+str(user_id),"u:"+str(from_user_id)+message_info_id)
                else:
                    timeline_client.lpush(USER_MESSAGE_TIME_LINE_PREFIX+str(user_id),"u:"+str(from_user_id)+message_info_id)
                timeline_client.ltrim(USER_MESSAGE_TIME_LINE_PREFIX+str(user_id),0,40)
                if not timeline_client.exists(USER_MESSAGE_PREFIX+"u:"+str(user_id)+message_info_id):
                    timeline_client.hmset(USER_MESSAGE_PREFIX+"u:"+str(user_id)+message_info_id,{"message_type":message_type,"content_id":contentid,\
                        "content":json.dumps(content),"addtime":addtime,"status":status,"fuser_id":from_user_id,"tuser_id":user_id})   
                if not only_all and not status:
                    add_to_unread_message_timeline(message_type,contentid,content,from_user_id,touser_id,taddtime)
    else:
        if not lpush:
             timeline_client.rpush(USER_MESSAGE_TIME_LINE_PREFIX+str(touser_id),"u:"+str(from_user_id)+message_info_id)  
        else:
            timeline_client.lpush(USER_MESSAGE_TIME_LINE_PREFIX+str(touser_id),"u:"+str(from_user_id)+message_info_id)
        timeline_client.ltrim(USER_MESSAGE_TIME_LINE_PREFIX+str(touser_id),0,40)
        if not timeline_client.exists(USER_MESSAGE_PREFIX+"u:"+str(touser_id)+message_info_id):
            timeline_client.hmset(USER_MESSAGE_PREFIX+"u:"+str(touser_id)+message_info_id,{"message_type":message_type,"content_id":contentid,\
                "content":json.dumps(content), "addtime":addtime,"status":status,"fuser_id":from_user_id,"tuser_id":touser_id})
        #add_unread_message_count(touser_id)
        if  not only_all and not status:
            add_to_unread_message_timeline(message_type,contentid,content,from_user_id,touser_id,taddtime)

def add_to_unread_message_timeline(message_type,contentid,content,fuser_id,touser_id,addtime,addinfo=False,lpush=True,incr_unread=True):
    message_info_id="t:"+str(message_type)+"c:"+str(contentid)
    addtime=addtime.strftime(TIME_STRF)
    if message_type==1:
        question_id=content["question_id"]
        question_follow=get_question_follower(question_id)
        question_follow.add(int(content["question_user_id"]))
        for user_id in question_follow:
            if int(user_id)!=int(fuser_id):
                if incr_unread:
                    add_unread_message_count(user_id)
                if not lpush:
                    timeline_client.rpush(USER_UNREAD_MESSAGE_TIME_LINE_PREFIX+str(user_id),"u:"+str(fuser_id)+message_info_id)
                else:
                    timeline_client.lpush(USER_UNREAD_MESSAGE_TIME_LINE_PREFIX+str(user_id),"u:"+str(fuser_id)+message_info_id)
                timeline_client.ltrim(USER_UNREAD_MESSAGE_TIME_LINE_PREFIX+str(user_id),0,20)
                if  addinfo and not timeline_client.exists(USER_MESSAGE_PREFIX+"u:"+str(user_id)+message_info_id):
                    timeline_client.hmset(USER_MESSAGE_PREFIX+"u:"+str(user_id)+message_info_id,{"message_type":message_type,"content_id":contentid,\
                            "content":json.dumps(content), "addtime":addtime,"status":0,"fuser_id":fuser_id,"tuser_id":touser_id})
    else:
        if not lpush:
            timeline_client.rpush(USER_UNREAD_MESSAGE_TIME_LINE_PREFIX+str(touser_id),"u:"+str(fuser_id)+message_info_id)
        else:
            timeline_client.lpush(USER_UNREAD_MESSAGE_TIME_LINE_PREFIX+str(touser_id),"u:"+str(fuser_id)+message_info_id)
        timeline_client.ltrim(USER_UNREAD_MESSAGE_TIME_LINE_PREFIX+str(touser_id),0,20)
        if addinfo and not timeline_client.exists(USER_MESSAGE_PREFIX+"u:"+str(touser_id)+message_info_id):
            timeline_client.hmset(USER_MESSAGE_PREFIX+"u:"+str(touser_id)+message_info_id,{"message_type":message_type,"content_id":contentid,\
                    "content":json.dumps(content), "addtime":addtime,"status":0,"fuser_id":fuser_id,"tuser_id":touser_id})
        if incr_unread:
            add_unread_message_count(touser_id)

def read_message(content_id,message_type,user_id,fuser_id):
    message_info_id="t:"+str(message_type)+"c:"+str(content_id)
    if timeline_client.exists(USER_UNREAD_MESSAGE_TIME_LINE_PREFIX+str(user_id)):
        count=timeline_client.lrem(USER_UNREAD_MESSAGE_TIME_LINE_PREFIX+str(user_id),0,"u:"+str(fuser_id)+message_info_id)
        #import pdb;pdb.set_trace()
        if count:
            timeline_client.hset(USER_MESSAGE_PREFIX+"u:"+str(user_id)+message_info_id,"status",1)
            reduce_unread_message_count(user_id,message_type,content_id,update_mysql=True)
        else:
            count=Message.objects.filter(to_user_id=user_id,message_type=message_type,contentid=content_id).update(status=1)
            if count:
                reduce_unread_message_count(user_id,message_type,content_id)

def add_unread_message_count(user_id,incr=1):
    if timeline_client.exists(USER_UNREAD_MESSAGE_COUNT_PREFIX+str(user_id)):
        timeline_client.incrby(USER_UNREAD_MESSAGE_COUNT_PREFIX+str(user_id),incr)

def reduce_unread_message_count(user_id,message_type,content_id,update_mysql=None,reduc=1):
    if timeline_client.exists(USER_UNREAD_MESSAGE_COUNT_PREFIX+str(user_id)):
        timeline_client.decr(USER_UNREAD_MESSAGE_COUNT_PREFIX+str(user_id),reduc)
        if update_mysql:
            Message.objects.filter(to_user_id=user_id,message_type=message_type,contentid=content_id).update(status=1)

def add_info_to_timeline(user_id,activity_type,content_id,addtime,**kwargs): 
    if not (activity_type=="reply_answer" and activity_type=="reply_comment"):
        add_to_activity_timeline(user_id,activity_type,content_id,addtime,is_push=kwargs.get("is_push",True))
        add_to_event_timeline(user_id,activity_type,content_id,addtime)
    if not activity_type=="submit_question":
        add_to_message_timeline(user_id,activity_type,content_id,addtime,**kwargs)

def delete_from_message_timeline(user_id,activity_type,content_id,**kwargs):
    question_id=kwargs.get("question_id",None)
    delete_message(user_id,activity_type,content_id,question_id)

def delete_from_activity_timeline(user_id,activity_type,content_id):
    delete_activity(user_id,activity_type,content_id)


def delete_activity_from_timeline(user_id,activity_type,content_id,fuser_id):
    "删除动态"
    activity_info_id="t:"+str(activity_type)+"c:"+str(content_id)
    timeline_client.lrem(USER_ACTIVITY_TIME_LINE_PREFIX+str(user_id),0,"u:"+str(fuser_id)+activity_info_id)
    timeline_client.delete(USER_ACTIVITY_PREFIX+"u:"+str(user_id)+activity_info_id)

def delete_from_event_timeline(user_id,activity_type,content_id):
    delete_event(user_id,activity_type,content_id)
   
def delete_event(user_id,activity_type,content_id):
    event_info_id="t:"+activity_type+"c:"+content_id
    timeline_client.lrem(USER_EVENT_TIME_LINE_PREFIX+str(user_id),0,event_info_id)
    timeline_client.delete(USER_EVENT_PREFIX+str("u:"+user_id+event_info_id))

def delete_from_timeline(user_id,activity_type,content_id,**kwargs):
    delete_from_activity_timeline(user_id,activity_type,content_id)
    delete_from_message_timeline(user_id,activity_type,content_id,kwargs)
    delete_from_event_timeline(user_id,activity_type,content_id)

