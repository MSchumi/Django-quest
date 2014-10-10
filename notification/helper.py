#coding=utf-8
from redishelper.timeline import add_info_to_timeline
import redis


def public_message(user_id,activity_type,content_id,addtime,**kwargs):
    add_info_to_timeline(user_id,activity_type,content_id,addtime,**kwargs)



