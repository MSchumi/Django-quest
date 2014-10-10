#coding=utf-8
from time import sleep
import json
from datetime import datetime
import redis
from celery.task import task

from quest.models import QustionFollow
from redishelper.util import connect,get_next_event_id,get_next_activity_id,get_next_message_id,get_datetime
from redishelper.timeline import add_to_message_timeline
from notification.models import Message


USER_DB_NUM=1
TIME_LINE_DB_NUM=2
QUESTION_DB_NUM=3
QUESTION_FOLLOWER_PREFIX="question_follower:"
USER_FOLLOWER_PREFIX="follower:"
USER_ACTIVITY_PREFIX="activity:"
USER_MESSAGE_PREFIX="message:"
USER_EVENT_PREFIX="event:"
USER_ACTIVITY_TIME_LINE_PREFIX="activity_time_line:"
USER_MESSAGE_TIME_LINE_PREFIX="message_time_line:"
USER_EVENT_TIME_LINE_PREFIX="event_time_line:"
CURRENT_ACTIVITY_ID_PREFIX="current_activity_id"
CURRENT_EVENT_ID_PREFIX="current_event_id"
CURRENT_MESSAGE_ID_PREFIX="current_message_id"
ACTIVITY_TYPE={"submit_question":0,"add_answer":1,"follow_question":2,"evaluate_answer":3,"reply_answer":4,"reply_comment":5,"follow_user":6}

TIME_STRF="%Y/%m/%d %H:%M:%S"


@task()
def insert_message(message_type,contentid,fuser_id,touser_id,content_dict):
    addtime=datetime.now()
    content={}
    content["addtime"]=addtime.strftime(TIME_STRF)
    content["user_id"]=fuser_id
    content["user_name"]=content_dict["user_name"]
    Message_list=[] 
    fields=['message_type','contentid','content','from_user_id','to_user_id','addtime','status'] 
    if message_type==6:
        Message_list=[(message_type,contentid,json.dumps(content),fuser_id,touser_id,addtime)]
    else:
        if message_type==1 or message_type==2:
            question_id=content_dict["question_id"]
            content["question_id"]=question_id
            content["question_title"]=content_dict["question_title"]
            if message_type==1:
                content["answer_id"]=contentid
                content["question_user_id"]=int(content_dict["question_user_id"])
                #question_user_id=content_dict["question_user_id"]
                question_followers=QustionFollow.objects.filter(question_id=question_id).values("user_id")
                Message_list=[(message_type,contentid,json.dumps(content),fuser_id,touser_id,addtime,0)for follow in question_followers for userid in\
                        follow.values() if userid!=int(fuser_id)  ]
                Message_list.append((message_type,contentid,json.dumps(content),fuser_id,int(content_dict["question_user_id"]),addtime,0))
            else:
                Message_list=[(message_type,contentid,json.dumps(content),fuser_id,touser_id,addtime,0)]
        else:
            content["question_id"]=content_dict["question_id"]
            content["answer_id"]=content_dict["answer_id"]
            if message_type==3:
                content["evaluate_answer_id"]=contentid
                content["answer_content"]=content_dict["answer_content"]
                content["status"]=content_dict["status"]
            elif message_type==4:
                content["answer_id"]=content_dict["answer_id"]
                content["answer_content"]=content_dict["answer_content"]
                content["comment_id"]=contentid
            elif message_type==5:
                content["comment_id"]=contentid
                content["answer_content"]=content_dict["answer_content"]
                content["comment_content"]=content_dict["commnet_content"]
            Message_list=[(message_type,contentid,json.dumps(content),fuser_id,touser_id,addtime,0)]
    if Message_list:
        add_to_message_timeline(message_type,contentid,content,fuser_id,touser_id,addtime,status=0)
        Message.messageobjects.bulk_insert_ignore(fields,Message_list)
    return addtime
            






    




