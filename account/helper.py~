#coding=utf-8
from account.models import UserFollow,User,Register_Temp
from account.signals import  register_user_done,follow_user_done
from redishelper.user import follow_user_in_redis,delete_follow_in_reids


def follow_user(tuser,ftype,user):
    follow_id=None
    if ftype=="0":
        follow_id=UserFollow.objects.create(ufollow=user,tuser=tuser).id
        follow_user_in_redis(user.id,tuser.id)
    else:
        follow=UserFollow.objects.filter(ufollow=user,tuser=tuser)
        follow_id=follow.id
        follow.delete()
        delete_follow_in_reids(user.id,tuser.id)
    follow_user_done.send(sender=UserFollow,fuser=user,tuser=tuser,optype=ftype,follow_id=follow_id)
    return True

def create_user(email,password,name,surname,activecode):
    user=User.objects.create_user(email=email,password=password,name=name,surname=surname)
    temp=Register_Temp.objects.create(email=email,activecode=activecode)
    register_user_done.send(sender=User,instance=user)
    return True



