#coding:utf-8
import json
from datetime import datetime

from quest.signals import question_submit_done,answer_submit_done,vote_submit_done,follow_question_done
from quest.models import Event,EventContent,Question,Answer,AnswerEvaluation,QustionFollow
from redishelper.timeline import add_to_event_timeline

def save_event(userid,eventtype,content,contentid,add=True,update=True):
    #import pdb;pdb.set_trace()
    "保存个人动态"
    try:
        event=Event.objects.filter(user_id=userid,eventtype=eventtype,contentid=contentid)
        if add:
            if len(event)>0:
                event=event[0]
                event.save()
                update=True
            else:
                event=Event(user_id=userid,eventtype=eventtype,contentid=contentid)
                event.save()
                update=False
        else:
            if len(event)>0:
                event[0].delete()
                event=event[0]
        #import pdb;pdb.set_trace()
        if event:
            add_to_event_timeline(userid,eventtype,contentid,event.addtime,event.id,add=add,update=update)
        return True
    except Exception,e:
        print e
        raise Exception
        return False

def submit_question(obj,user,**kwargs):
    "保存提交的问题动态 json存储方式现在废弃"
    event_content={"id":obj.id,"title":obj.title,"content":obj.content}
    save_event(user.id,0,event_content,obj.id)

def update_follwer():
    pass

def submit_answer(obj,user,question,**kwarg):
    #question=kwarg.pop('question',None)
    answer=obj
    #import pdb;pdb.set_trace()
    event_content={"id":answer.id,"content":answer.content,"question":{"id":question.id,"title":question.title,"content":\
            question.content,"opposecount": answer.opposecount,"favorcount":answer.opposecount,"commentcount":answer.commentcount}}
    save_event(user.id,1,event_content,answer.id)

def vote_submit(instance,user,optype,**kwarg):
    if optype=="delete":
         save_event(user.id,3,"",instance,False)
    else:
        event_content={"id":instance.id,"content":instance.status,"answer":{"id":instance.answer.id,"content": \
                instance.answer.content,"opposecount": instance.answer.opposecount,"favorcount":instance.answer.opposecount,\
                "commentcount":instance.answer.commentcount},"question":{"id":instance.answer.question.id,"title":\
                instance.answer.question.title,"content":instance.answer.question.content}}
        save_event(user.id,3,event_content,instance.id)

def follow_question(instance,user,optype,**kwarg):
    if optype=="delete":
         save_event(user.id,2,"",instance,False)
    else:
        save_event(user.id,2,"",instance.id)

question_submit_done.connect(submit_question,sender=Question)
answer_submit_done.connect(submit_answer,sender=Answer)
vote_submit_done.connect(vote_submit,sender=AnswerEvaluation)
follow_question_done.connect(follow_question,sender=QustionFollow)

        


