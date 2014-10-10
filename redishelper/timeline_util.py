#coding=utf-8

import json
from datetime import datetime
from quest.models import Event,QustionFollow,AnswerEvaluation
from feed.models import Activity
from notification.models import Message

from redishelper.util import connect,get_next_event_id,get_next_activity_id,get_next_message_id,get_datetime
from redishelper.question import get_question_from_redis,get_answer_by_answer_id,load_question_follower
from redishelper.timeline import add_to_event_timeline,add_to_activity_timeline,delete_activity_from_timeline,add_to_unread_message_timeline,add_to_message_timeline
from redishelper.user import get_user_by_id,follow_question_to_user_set,cancle_follow_question_from_user_set
from redishelper.redisconfig import *

SPLIT_STR="t:"

def push_activity(user_id,activity_type,content_id,addtime):
    followers=user_client.smembers(USER_FOLLOWER_PREFIX+str(user_id))
    for follower in followers:
        add_to_activity_timeline(follower,activity_type,content_id,addtime,user_id)

def delete_activity(user_id,activity_type,content_id):
    followers=user_client.smembers(USER_FOLLOWER_PREFIX+str(user_id))
    for follower in followers:
        delete_activity_from_timeline(follower,activity_type,content_id,user_id)

def delete_event(user_id,activity_type,content_id):
    pass

def get_events_list(user_id,skip=0,count=-1):
    field=["id","activity_type","content_id","addtime"]
    items=[]
    question_submit_count=0
    answer_count=0
    if not timeline_client.exists(USER_EVENT_TIME_LINE_PREFIX+str(user_id)):
        events=Event.objects.filter(user_id=user_id)
        for event in events:
            add_to_event_timeline(user_id,event.eventtype,event.contentid,event.addtime,event.id,add=True,update=False,lpush=False)
    event_id_list=timeline_client.lrange(USER_EVENT_TIME_LINE_PREFIX+str(user_id),skip,skip+count)
    for event_info_id in event_id_list:
        #import pdb;pdb.set_trace()
        info=timeline_client.hmget(USER_EVENT_PREFIX+"u:"+str(user_id)+event_info_id,field)
        item,question_submit_count,answer_count=get_event(int(info[1]),info[2],get_datetime(info[3]),question_submit_count,answer_count)
        items.append(item)
    return {"event_list":items,"statistics":{"submit_question":question_submit_count,"answer":answer_count}}

def get_activities_list(user_id,skip=0,count=-1):
    field=["id","activity_type","content_id","addtime","fuser"]
    items=[]
    if not timeline_client.exists(USER_ACTIVITY_TIME_LINE_PREFIX+str(user_id)):
        activities=Activity.objects.filter(to_user=user_id)
        for activity in activities:
            add_to_activity_timeline(user_id,activity.activitytype,activity.contentid,activity.addtime,activity.from_user_id,lpush=False)
    activity_id_list=timeline_client.lrange(USER_ACTIVITY_TIME_LINE_PREFIX+str(user_id),skip,skip+count)
    for activity_info_id in activity_id_list:
        #import pdb;pdb.set_trace()
        activity_info_id="t:"+activity_info_id.split("t:")[1]
        info=timeline_client.hmget(USER_ACTIVITY_PREFIX+"u:"+str(user_id)+activity_info_id,field)
        if info:
            item=get_activity(int(info[1]),info[2],get_datetime(info[3]),int(info[4]))
            if item:
                items.append(item)
    #import pdb;pdb.set_trace()
    return {"activity_list":items,"statistics":{"submit_question":0,"answer":0}}

def get_message_list(user_id,endtime=None,skip=0,count=-1):
    field=["message_type","content_id","content","status","addtime","fuser_id"]
    items=[]
    if skip<40:
        if not timeline_client.exists(USER_MESSAGE_TIME_LINE_PREFIX+str(user_id)):
            messages=Message.objects.filter(to_user=user_id)[0:40]
            for message in messages:
                add_to_message_timeline(message.message_type,message.contentid,json.loads(message.content),message.from_user_id,user_id,message.addtime,\
                        status=message.status,only_all=True,lpush=False)
        message_id_list=timeline_client.lrange(USER_MESSAGE_TIME_LINE_PREFIX+str(user_id),skip,skip+count)
        for message_info_id in message_id_list:
            message_info_id="t:"+message_info_id.split("t:")[1]
            info=timeline_client.hmget(USER_MESSAGE_PREFIX+"u:"+str(user_id)+message_info_id,field) 
            if info:
                item=get_message(info[0],info[3],info[2],info[5],get_datetime(info[4]),info[1])
                if item:
                    items.append(item)
    else:  
        messages=Message.objects.filter(to_user=user_id,addtime__lt=endtime)[0:20]
        for message in messages:
            item=get_message(message.message_type,message.status,message.content,message.from_user_id,message.addtime,message.contentid)
            items.append(item)
    endtime=None
    if items:
        endtime=items[-1]["addtime"]
    return {"messages":items,"unread_count":get_unread_message_count(user_id),"endtime":endtime,"count":len(items)}

def get_unread_message_list(user_id,endtime=None,skip=0,count=-1):
    field=["message_type","content_id","content","status","addtime","fuser_id"]
    items=[]
    if skip<40:
        if not timeline_client.exists(USER_UNREAD_MESSAGE_TIME_LINE_PREFIX+str(user_id)):
            messages=Message.objects.filter(to_user=user_id,status=0)[0:20]
            for message in messages:
                add_to_unread_message_timeline(message.message_type,message.contentid,json.loads(message.content),message.from_user_id,user_id,\
                        message.addtime,True,lpush=False,incr_unread=False)
        message_id_list=timeline_client.lrange(USER_UNREAD_MESSAGE_TIME_LINE_PREFIX+str(user_id),skip,skip+count)
        #import pdb;pdb.set_trace()
        for message_info_id in message_id_list: 
            message_info_id="t:"+message_info_id.split("t:")[1]
            info=timeline_client.hmget(USER_MESSAGE_PREFIX+"u:"+str(user_id)+message_info_id,field)
            if info:
                item=get_message(info[0],info[3],info[2],info[5],get_datetime(info[4]),info[1])
                if item:
                    items.append(item)
    else:
        messages=Message.objects.filter(to_user=user_id,status=0,addtime__lt=endtime)[0:20]
        for message in messages:
            item=get_message(message.message_type,message.status,message.content,message.from_user_id,message.addtime,message.contentid)
            items.append(item)
    endtime=None
    if items:
        endtime=items[-1]["addtime"]
    return {"messages":items,"unread_count":get_unread_message_count(user_id),"endtime":endtime,"count":len(items)}

def get_unread_message_count(user_id):
    if not timeline_client.exists(USER_UNREAD_MESSAGE_COUNT_PREFIX+str(user_id)):
        count=Message.objects.filter(status=0,to_user_id=int(user_id)).count()
        timeline_client.set(USER_UNREAD_MESSAGE_COUNT_PREFIX+str(user_id),count)
        return count
    count=timeline_client.get(USER_UNREAD_MESSAGE_COUNT_PREFIX+str(user_id))
    return int(count)

def get_message(message_type,status,content,fuser_id,addtime,content_id):
    item={"message_type":int(message_type),"status":int(status),"content_id":int(content_id),"content":json.loads(content),"addtime":addtime,"fuser_id":fuser_id}
    return item

def get_activity(activity_type,content_id,addtime,fuser):
    item={}
    fuser=get_user_by_id(fuser)
    if activity_type==0:
        question=get_question_from_redis(content_id)
        if question:
            item={'activitytype':activity_type,'addtime':addtime,"data":question,"fuser":fuser}
    elif activity_type==1:
        answer=get_answer_by_answer_id(content_id)
        if answer:
            item={'activitytype':activity_type,'addtime':addtime,"data":answer,"fuser":fuser}
    elif activity_type==2:
        follow=QustionFollow.objects.filter(pk=content_id)#如何解决
        follow=follow[0] if len(follow)>0 else None
        if not follow:
            return None
        question=question=get_question_from_redis(follow.question_id)
        follow.question=question
        item={'activitytype':activity_type,'addtime':addtime,"data":follow,"fuser":fuser}
    elif activity_type==3:
        evalue=AnswerEvaluation.objects.filter(pk=content_id)
        evalue=evalue[0] if len(evalue)>0 else None
        if not evalue:
            return None
        answer=get_answer_by_answer_id(evalue.answer_id)
        evalue.answer=answer
        item={'activitytype':activity_type,'addtime':addtime,"data":evalue,"fuser":fuser}
    return item

def get_event(event_type,content_id,addtime,question_submit_count,answer_count):
    item={}
    if event_type==0:
        question=get_question_from_redis(content_id)
        item={'eventtype':event_type,'addtime':addtime,"data":question}
        question_submit_count+=1
    elif event_type==1:
        answer=get_answer_by_answer_id(content_id)
        item={'eventtype':event_type,'addtime':addtime,"data":answer}
        answer_count +=1
    elif event_type==2:
        follow=QustionFollow.objects.get(pk=content_id)#如何解决 
        question=question=get_question_from_redis(follow.question_id)
        follow.question=question
        item={'eventtype':event_type,'addtime':addtime,"data":follow}
    elif event_type==3:
        evalue=AnswerEvaluation.objects.get(pk=content_id)
        answer=get_answer_by_answer_id(evalue.answer_id)
        evalue.answer=answer
        item={'eventtype':event_type,'addtime':addtime,"data":evalue}
    return (item,question_submit_count,answer_count)

def follow_question(question_id,user_id):
    if not question_client.exists(QUESTION_FOLLOWER_PREFIX+str(question_id)):
        load_question_follower(question_id)
        question_client.sadd(QUESTION_FOLLOWER_PREFIX+str(question_id),user_id)
    follow_question_to_user_set(question_id,user_id)
    
def cancle_follow_question(question_id,user_id):
    if question_client.exists(QUESTION_FOLLOWER_PREFIX+str(question_id)):
        question_client.srem(QUESTION_FOLLOWER_PREFIX+str(question_id),user_id)
    delete_activity(user_id,2,question_id)
    cancle_follow_question_from_user_set(question_id,user_id)
