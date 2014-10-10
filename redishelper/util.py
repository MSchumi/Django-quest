#coding=utf-8

import time
from datetime import datetime
from django.db.models import Max
from django.conf import settings 

import redis

from notification.models import Message
from quest.models import Event,Question,Answer,Comment,AnswerEvaluation,CommentEvaluation,QustionFollow
from feed.models import Activity
from redishelper.redisconfig import *

def connect(db_num):
    if not db_num:
        db_num=0
    try:
        db_num=int(db_num)
        if db_num>15 or db_num<0:
            raise Exception(u"超过了数据库索引范围")
    except:
        raise Exception(u"数据库设置错误")
    client=redis.StrictRedis(host=settings.REDIS_IP,port=settings.REDIS_PORT,db=db_num)
    return client

def get_next_id(cls,client,key):
    if not client.exists(key):
        #import pdb;pdb.set_trace()
        max_id=cls.objects.aggregate(Max('id')).get("id__max",0)
        if not max_id:
            max_id=0
        client.set(key,int(max_id)+1)
        return int(max_id)+1
    else:
        max_id=client.incr(key)
        return max_id

def get_datetime(date_str):
    t=time.strptime(date_str,TIME_STRF)
    return datetime(* t[:6])

def get_next_event_id():
    return get_next_id(Event,timeline_client,CURRENT_EVENT_ID_PREFIX)

def get_next_activity_id():
    return get_next_id(Activity,timeline_client,CURRENT_ACTIVITY_ID_PREFIX)

def get_next_message_id():
    return get_next_id(Message,timeline_client,CURRENT_MESSAGE_ID_PREFIX)

def get_next_question_id():
    return get_next_id(Question,question_client,CURRENT_QUESTION_ID_PREDIX)

def get_next_answer_id():
    return get_next_id(Answer,question_client,CURRENT_ANSWER_ID_PREDIX)

def get_next_comment_id():
    return get_next_id(Comment,question_client,CURRENT_COMMENT_ID_PREDIX)

def get_next_question_follow_id():
    return get_next_id(QustionFollow,question_client,CURRENT_QUESTION_FOLLOW_ID_PREDIX)

def get_next_answer_evaluation_id():
    return get_next_id(AnswerEvaluation,question_client,CURRENT_ANSWER_EVALUATION_ID_PREDIX)

def get_next_comment_evaluation_id():
    return get_next_id(CommentEvaluation,question_client,CURRENT_COMMENT_EVALUATION_ID_PREDIX)
