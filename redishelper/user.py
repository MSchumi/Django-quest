#coding=utf-8

from django.conf import settings 
import redis

from account.models import User,UserFollow 
from quest.models import QustionFollow,AnswerEvaluation
from redishelper.redisconfig import *


def is_exists(email):
    if user_client.exists(EMAIL_LIST_PREFIX+email):
        return True
    else:
        return False

def load_user_hash(user):
    try:
        user_client.set(EMAIL_LIST_PREFIX+user.email,user.id)
        user_client.hmset(USER_HASH_PREFIX+str(user.id),{"name":user.name.encode("utf-8"),"surname":user.surname.encode("utf-8"),"email":user.email,\
                "avatar":user.avatar,"password":user.password,"is_active":str(user.is_active)})
    except Exception,e:
        raise Exception(u"redis用户设置错误"+e)

def update_avtar(user_id,path):
    "修改用户头像"
    if user_client.exists(USER_HASH_PREFIX+str(user_id)):
        user_client.hset(USER_HASH_PREFIX+str(user_id),"avatar",path)

def load_user_follow(user_id):
    #import pdb;pdb.set_trace()
    if not user_client.exists(USER_FOLLOW_PREFIX+str(user_id)):
        follows=UserFollow.objects.filter(ufollow_id=user_id).values("tuser_id")
        follow_id=[v for follow in follows for k,v in follow.items()]
        follow_id.append(-1)
        if follow_id:
            user_client.sadd(USER_FOLLOW_PREFIX+str(user_id),*follow_id)

def load_user_follower(user_id):
    if not user_client.exists(USER_FOLLOWER_PREFIX+str(user_id)):
        followers=UserFollow.objects.filter(tuser_id=user_id).values("ufollow_id")
        follower_id=[v for follower in followers for k,v in follower.items()]
        follower_id.append(-1)
        if follower_id:
            user_client.sadd(USER_FOLLOWER_PREFIX+str(user_id),*follower_id)

def get_user_email(email):
    keys=['name','surname','password','avatar']
    if user_client.exists(EMAIL_LIST_PREFIX+email):
        user_id=user_client.get(EMAIL_LIST_PREFIX+email)
        user_info=user_client.hmget(USER_HASH_PREFIX+str(user_id),keys)
        user=User(id=user_id,name=user_info[0],surname=user_info[1],password=user_info[2],email=email,avatar=user_info[3])
        return [user]
    else:
        user=User.objects.filter(email=email)
        if len(user)==0:
            return []
        else:
            load_user_hash(user[0])
            return user

def get_user_by_id(user_id):
    load_user_info(user_id)
    keys=['name','surname','password','email','avatar','is_active']
    if user_client.exists(USER_HASH_PREFIX+str(user_id)):
        user_info=user_client.hmget(USER_HASH_PREFIX+str(user_id),keys)
        user=User(id=int(user_id),name=user_info[0].decode("utf-8"),surname=user_info[1].decode("utf-8"),password=user_info[2],email=user_info[3],\
                avatar=user_info[4],is_active=bool(user_info[5]))
        return user
    else:
        try:
            user=User.objects.get(pk=user_id)
            load_user(user)
            return user
        except:
            return None

def load_user_info(user_id):
    load_user_follow(user_id)
    load_user_follower(user_id)
    load_follow_question(user_id)   
    load_evaluation_for_answer(user_id)


def load_user(user):
    load_user_hash(user)
    load_user_info(user.id)
    

def load_follow_question(user_id):
    if not user_client.exists(USER_FOLLOW_QUESTION_PREFIX+str(user_id)):
        questions=QustionFollow.objects.filter(user_id=user_id).values("question_id")
        question_id=[v for question in questions for _,v in question.items()]
        question_id.append(-1)
        if question_id:
            user_client.sadd(USER_FOLLOW_QUESTION_PREFIX+str(user_id),*question_id)

def load_favor_answer(user_id):
    "加载用户赞过的回答"
    if not question_client.exists(USER_FAVOR_ANSWER_PREFIX+str(user_id)):
        answers=AnswerEvaluation.objects.filter(user_id=user_id,status=FAVOR_ANSWER).values("answer_id")
        answers_id=[v for answer in answers for _,v in answer.items()]
        answers_id.append(-1)
        if answers_id:
            question_client.sadd(USER_FAVOR_ANSWER_PREFIX+str(user_id),*answers_id)

def load_oppose_answer(user_id):
    "加载用户反对过得回答"
    if not question_client.exists(USER_OPPOSE_ANSWER_PREFIX+str(user_id)):
        answers=AnswerEvaluation.objects.filter(user_id=user_id,status=OPPOSE_ANSWER).values("answer_id")
        answers_id=[v for answer in answers for _,v in answer.items()]
        answers_id.append(-1)
        if answers_id:
            question_client.sadd(USER_OPPOSE_ANSWER_PREFIX+str(user_id),*answers_id)

def load_evaluation_for_answer(user_id):
    load_oppose_answer(user_id)
    load_favor_answer(user_id)

def is_follow(user_id,tuser_id):
    if not user_client.exists(USER_FOLLOW_PREFIX+str(user_id)):
        load_user_info(user_id)
    if user_client.sismember(USER_FOLLOW_PREFIX+str(user_id),tuser_id):
        return True
    return False

def follow_user_in_redis(user_id,tuser_id):
    "添加关注的好友"
    if user_client.exists(USER_FOLLOW_PREFIX+str(user_id)):
        user_client.sadd(USER_FOLLOW_PREFIX+str(user_id),tuser_id)
    if user_client.exists(USER_FOLLOWER_PREFIX+str(tuser_id)):
        user_client.sadd(USER_FOLLOWER_PREFIX+str(tuser_id),user_id)

def delete_follow_in_reids(user_id,tuser_id):
    "删除关注的好友"
    if user_client.exists(USER_FOLLOW_PREFIX+str(user_id)):
        user_client.srem(USER_FOLLOW_PREFIX+str(user_id),tuser_id)

def is_follow_question(question_id,user_id):
    if user_client.sismember(USER_FOLLOW_QUESTION_PREFIX+str(user_id),question_id):
        return True
    else:
        return False

def follow_question_to_user_set(question_id,user_id):
    if not user_client.exists(USER_FOLLOW_QUESTION_PREFIX+str(user_id)):
        load_follow_question(user_id)
    user_client.sadd(USER_FOLLOW_QUESTION_PREFIX+str(user_id),question_id)

def cancle_follow_question_from_user_set(question_id,user_id):
    if user_client.exists(USER_FOLLOW_QUESTION_PREFIX+str(user_id)):
        user_client.srem(USER_FOLLOW_QUESTION_PREFIX+str(user_id),question_id)





