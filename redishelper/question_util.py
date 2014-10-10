#coding=utf-8
from datetime import datetime

import redis
from quest.models import Event,QustionFollow
from redishelper.util import (connect,get_next_question_id,get_next_answer_id,get_next_comment_id,get_next_question_follow_id,
        get_next_answer_evaluation_id,get_next_comment_evaluation_id,get_datetime)
from redishelper.redisconfig import *

def load_question_follower(question_id):
    client=connect(QUESTION_DB_NUM)
    if not client.exists(QUESTION_FOLLOWER_PREFIX+str(question_id)):
        users=QustionFollow.objects.filter(question_id=question_id).values("user_id")
        users_id=[v for user in users for _,v in user.items()]
        users_id.append(-1)
        client.sadd(QUESTION_FOLLOWER_PREFIX+str(question_id),*users_id)
        users_id.remove(-1)
        return set(users_id)
    users_set=client.smembers(QUESTION_FOLLOWER_PREFIX+str(question_id))
    users_set.remove(-1)
    return users_set

def get_question_follower(question_id):
    #import pdb;pdb.set_trace()
    client=connect(QUESTION_DB_NUM)
    if not client.exists(QUESTION_FOLLOWER_PREFIX+str(question_id)):
        return load_question_follower(question_id)
    users_set=client.smembers(QUESTION_FOLLOWER_PREFIX+str(question_id))
    #users_set.remove(-1)
    users_set.remove("-1")
    return users_set
