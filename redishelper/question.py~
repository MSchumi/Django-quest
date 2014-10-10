#coding=utf-8

from datetime import datetime

import redis
from quest.models import Question,QustionFollow,Answer,Comment,AnswerEvaluation,Event
from account.models import User
from redishelper.redisconfig import *
from redishelper.util import *
from redishelper.user import load_user,get_user_by_id,load_favor_answer,load_oppose_answer,follow_question_to_user_set,cancle_follow_question_from_user_set
from redishelper.timeline import delete_from_timeline 

def load_question_follower(question_id):
    if not question_client.exists(QUESTION_FOLLOWER_PREFIX+str(question_id)):
        users=QustionFollow.objects.filter(question_id=question_id).values("user_id")
        users_id=[v for user in users for _,v in user.items()]
        users_id.append(-1)
        question_client.sadd(QUESTION_FOLLOWER_PREFIX+str(question_id),*users_id)
        return users_id
    return question_client.smembers(QUESTION_FOLLOWER_PREFIX+str(question_id))

def load_question_by_id(question_id):
    question=Question.objects.select_related('user').get(pk=question_id)
    load_question_by_question(question)
    return question
   
def load_question_by_question(question):
    if not question_client.exists(QUESTION_PRFIX+str(question.id)):
        question_dict={"id":question.id,"title":question.title.encode('utf-8'),"content":question.content.encode('utf-8'),"answercount":question.answercount,\
                "addtime":question.addtime.strftime(TIME_STRF),"user_id":question.user.id}
        question_client.hmset(QUESTION_PRFIX+str(question.id),question_dict)
        load_user(question.user)
        load_question_follower(question.id)
        load_question_answer_by_answers(question.id,question.answer_set.select_related("user").all())

def load_answer_by_answer(answer):
    if not question_client.exists(QUESTION_ANSWER_PREFIX+str(answer.question_id)):
        load_question_by_id(answer.question_id)
    else:
        question_client.rpush(QUESTION_ANSWER_PREFIX+str(answer.question_id),answer.id)
        answer_dict={"id":answer.id,"question_id":answer.question_id,"content":answer.content,"addtime":answer.addtime.strftime(TIME_STRF),\
                "user_id":answer.user.id,"commentcount":answer.commentcount,"favorcount":answer.favorcount,"opposecount":answer.opposecount}
        question_client.hmset(ANSWER_PRFIX+str(answer.id),answer_dict)
        load_user(answer.user)

def load_answer_by_id(answer_id):
    answer=Answer.objects.select_related('user','question').filter(pk=answer_id)
    if not answer:
        return None
    load_answer_by_answer(answer[0])
    return answer[0]
    

def load_question_answer_by_id(question_id):
    answers=Answer.objects.select_related('user').filter(question_id=question_id).order_by('addtime')
    load_question_answer_by_answers(question_id,answers)
    return answers

def load_question_answer_by_answers(question_id,answers):
    if not question_client.exists(QUESTION_ANSWER_PREFIX+str(question_id)):
        #answer_id=[(answers[i].id,i) for i in range(len(answers))]
        answer_id=[answer.id for answer in answers]
        answer_id.insert(0,-1)
        question_client.rpush(QUESTION_ANSWER_PREFIX+str(question_id),*answer_id)
        for answer in answers:
            answer_dict={"id":answer.id,"content":answer.content,"addtime":answer.addtime.strftime(TIME_STRF),"user_id":answer.user.id,\
                    "commentcount":answer.commentcount,"favorcount":answer.favorcount,"opposecount":answer.opposecount,"question_id":answer.question_id}
            question_client.hmset(ANSWER_PRFIX+str(answer.id),answer_dict)
            load_user(answer.user)
            load_answer_evluation_by_evluations(answer.id,answer.answerevaluation_set.select_related('user').all())

def load_answer_evluation_by_id(answer_id):
    evluations=AnswerEvaluation.objects.filter(answer_id=answer_id)
    load_answer_evluation_by_evluations(answer_id,evluations)
    
def load_answer_evluation_by_evluations(answer_id,evluations):
    if not question_client.exists(ANSWER_EVALUATION_PREFIX+str(answer_id)):
        user_id=[evluation.user.id for evluation in evluations]
        user_id.append(-1)
        question_client.sadd(ANSWER_EVALUATION_PREFIX+str(answer_id),*user_id)
        for evluation in evluations:
            evluation_dict={"id":evluation.id,"edittime":evluation.edittime.strftime(TIME_STRF),"status":evluation.status,"user_id":evluation.user.id}
            question_client.hmset(ANSWEREVALUATION_PRFIX+"a:"+str(answer_id)+"u:"+str(evluation.user.id),evluation_dict)
            if evluation.status==1:
                question_client.sadd(FAVOUR_ANSWEREVALUATION_PRFIX+str(answer_id),evluation.user.id)
            else:
                question_client.sadd(OPPOSE_ANSWEREVALUATION_PRFIX+str(answer_id),evluation.user.id)
            load_user(evluation.user)

def load_comment_by_comments(answer_id,comments):
    if not question_client.exists(ANSWER_COMMENT_PREFIX+str(answer_id)):
        comment_id=[comment.id for comment in comments]
        comment_id.insert(-1,0)
        question_client.rpush(ANSWER_COMMENT_PREFIX+str(answer_id),*comment_id)
        for comment in comments:
            comment_dict={"id":comment.id,"answer_id":answer_id,"content":comment.content,"addtime":comment.addtime,"user":comment.user.id,\
                    "touser":comment.touser.id,"favorcount":comment.favorcount}
            load_user(comment.user)
            load_user(comment.touser)
            question_client.hmset(COMMENT_PRFIX+str(comment.id),comment_dict)

def load_comment_by_comment(comment):
    if not question_client.exists(ANSWER_COMMENT_PREFIX+str(comment.answer_id)):
        load_comment_by_answer_id(comment.answer_id)
    question_client.rpush(ANSWER_COMMENT_PREFIX+str(comment.answer_id),comment.id)
    comment_dict={"id":comment.id,"answer_id":comment.answer_id,"content":comment.content,"addtime":comment.addtime,"user":comment.user.id,\
                    "touser":comment.touser.id,"favorcount":comment.favorcount}
    load_user(comment.user)
    load_user(comment.touser)
    question_client.hmset(COMMENT_PRFIX+str(comment.id),comment_dict)


def load_comment_by_answer_id(answer_id):
    comments=Comment.objects.select_related("user","touser").filter(answer_id=answer_id)
    load_comment_by_comments(answer_id,comments)

def get_question_from_redis(question_id):
    field=["id","title","content","answercount","addtime","user_id"]
    if not question_client.exists(QUESTION_PRFIX+str(question_id)):
        return load_question_by_id(question_id)
    else:
        question_dict=question_client.hmget(QUESTION_PRFIX+str(question_id),field)
        question=Question(id=question_dict[0],title=question_dict[1].decode("utf-8"),content=question_dict[2].decode("utf-8"),answercount=int(question_dict[3]),\
                addtime=get_datetime(question_dict[4]),user=get_user_by_id(int(question_dict[5])))
        return question

def get_answer_by_answer_id(answer_id):
    field=["id","content","addtime","user_id","commentcount","favorcount","opposecount","question_id"]
    if not question_client.exists(ANSWER_PRFIX+str(answer_id)):
        return load_answer_by_id(answer_id)
    else:
        answer=question_client.hmget(ANSWER_PRFIX+str(answer_id),field)
        an=Answer(id=answer[0],content=answer[1],addtime=get_datetime(answer[2]),user=get_user_by_id(answer[3]),commentcount=int(answer[4]),favorcount=\
                int(answer[5]),opposecount=int(answer[6]),question=get_question_from_redis(answer[7]))
        return an

def get_answerevaluation_by_id(evaluation_id):
    pass

def get_question_follower(question_id):
    if not question_client.exists(QUESTION_FOLLOWER_PREFIX+str(question_id)):
        return load_question_follower(question_id)
    return question_client.smembers(QUESTION_FOLLOWER_PREFIX+str(question_id))

def get_answers_from_redis(question_id,limit=0,skip=0,user_id=None):
    field=["id","content","addtime","user_id","commentcount","favorcount","opposecount"]
    if not question_client.exists(QUESTION_ANSWER_PREFIX+str(question_id)):
        load_question_answer_by_id(question_id)
    answer_id=None
    if limit:
        answer_id=question_client.lrange(QUESTION_ANSWER_PREFIX+str(question_id),skip+1,limit+skip+1)
    else:
        answer_id=question_client.lrange(QUESTION_ANSWER_PREFIX+str(question_id),0,-1)
    answer_id=[i for i in answer_id if i!="-1" ]
    if answer_id:
        answers=[]
        answer_list=[question_client.hmget(ANSWER_PRFIX+str(i),field) for i in answer_id if i!='-1']
        for answer in answer_list:
            an=Answer(id=answer[0],content=answer[1],addtime=get_datetime(answer[2]),user=get_user_by_id(answer[3]),commentcount=int(answer[4]),favorcount=\
                int(answer[5]),opposecount=int(answer[6]))
            answers.append(an)
        if user_id:
            if not question_client.exists(USER_FAVOR_ANSWER_PREFIX+str(user_id)):
                load_favor_answer(user_id) 
            question_client.sadd(TEMP_PREFIX+str(user_id),*answer_id)
            #import pdb;pdb.set_trace()
            favors=question_client.sinter(TEMP_PREFIX+str(user_id),USER_FAVOR_ANSWER_PREFIX+str(user_id))
            for favor in favors:
                 for answer in answers:
                    if answer.id==favor:
                        answer.evaluation=1
                        answer.eid=int(question_client.hget(ANSWEREVALUATION_PRFIX+"a:"+str(answer.id)+"u:"+str(user_id),"id"))
            if not question_client.exists(USER_FAVOR_ANSWER_PREFIX+str(user_id)):
                 load_oppose_answer(user_id)
            opposes=question_client.sinter(TEMP_PREFIX+str(user_id),USER_OPPOSE_ANSWER_PREFIX+str(user_id))
            for oppose in opposes:
                for answer in answers:
                    if answer.id==oppose:
                        answer.evaluation=2
                        answer.eid=int(question_client.hget(ANSWEREVALUATION_PRFIX+"a:"+str(answer.id)+"u:"+str(user_id),"id"))
            question_client.delete(TEMP_PREFIX+str(user_id))
        return answers
    return None

def evaluate_answer(answer_id,user_id,status,evaluation_id=None,cancel=False):
    #import pdb;pdb.set_trace()
    if cancel:
        if question_client.exists(ANSWER_EVALUATION_PREFIX+str(answer_id)):
            question_client.srem(ANSWER_EVALUATION_PREFIX+str(answer_id),0,user_id)
            question_client.delete(ANSWEREVALUATION_PRFIX+ "a:"+str(answer_id)+"u:"+str(user_id)) 
            if status==FAVOR_ANSWER:
                question_client.srem(FAVOUR_ANSWEREVALUATION_PRFIX+str(answer_id),user_id)
            else:
                question_client.srem(OPPOSE_ANSWEREVALUATION_PRFIX+str(answer_id),user_id)
        #用户赞和反对过得回答set中删除
        if question_client.exists(USER_FAVOR_ANSWER_PREFIX+str(user_id)):
            if  question_client==FAVOR_ANSWER:
                question_client.srem(USER_FAVOR_ANSWER_PREFIX+str(user_id),answer_id)
            else:
                question_client.srem(USER_OPPOSE_ANSWER_PREFIX+str(user_id),answer_id)
               
    else:
        #import pdb;pdb.set_trace()
        if not question_client.exists(ANSWEREVALUATION_PRFIX+str(answer_id)):
            load_answer_evluation_by_id(answer_id)
        if not evaluation_id: #add
            evaluation_id=get_next_answer_evaluation_id()
            question_client.sadd(ANSWER_EVALUATION_PREFIX+str(answer_id),user_id)
            #import pdb;pdb.set_trace()
            evluation_dict={"id":evaluation_id,"edittime":datetime.now().strftime(TIME_STRF),"status":status,"user_id":user_id}
            question_client.hmset(ANSWEREVALUATION_PRFIX+ "a:"+str(answer_id)+"u:"+str(user_id),evluation_dict)
            if status==FAVOR_ANSWER:
                question_client.sadd(FAVOUR_ANSWEREVALUATION_PRFIX+str(answer_id),user_id)
                question_client.sadd(USER_FAVOR_ANSWER_PREFIX+str(user_id),answer_id)
            else:
                question_client.sadd(OPPOSE_ANSWEREVALUATION_PRFIX+str(answer_id),user_id)
                question_client.sadd(USER_OPPOSE_ANSWER_PREFIX+str(user_id),answer_id)
        else:# update
            evluation_dict={"id":evaluation_id,"edittime":datetime.now().strftime(TIME_STRF),"status":status,"user_id":user_id}
            question_client.hmset(ANSWEREVALUATION_PRFIX+ "a:"+str(answer_id)+"u:"+str(user_id),evluation_dict)
            if status==FAVOR_ANSWER:
                question_client.srem(OPPOSE_ANSWEREVALUATION_PRFIX+str(answer_id),user_id)
                question_client.sadd(FAVOUR_ANSWEREVALUATION_PRFIX+str(answer_id),user_id)
                question_client.srem(USER_OPPOSE_ANSWER_PREFIX+str(user_id),answer_id)
                question_client.sadd(USER_FAVOR_ANSWER_PREFIX+str(user_id),answer_id)
            else:
                question_client.srem(FAVOUR_ANSWEREVALUATION_PRFIX+str(answer_id),user_id)
                question_client.sadd(OPPOSE_ANSWEREVALUATION_PRFIX+str(answer_id),user_id)
                question_client.srem(USER_FAVOR_ANSWER_PREFIX+str(user_id),answer_id)
                question_client.sadd(USER_OPPOSE_ANSWER_PREFIX+str(user_id),answer_id)
    return evaluation_id

def submit_question(**kwargs):
    question=Question(**kwargs)
    question_id=get_next_question_id()
    question.id=question_id
    question.addtime=datetime.now()
    load_question_by_question(question)
    return question_id

def update_question(question_id,**kwargs):
    if question_client.exists(QUESTION_PRFIX+str(question_id)):
        question_client.hmset(QUESTION_PRFIX+str(question_id),kwargs)

def update_answer(**kwargs):
    if question_client.exists(ANSWER_PRFIX+str(kwargs["id"])):
        question_client.hmset(ANSWER_PRFIX+str(kwargs["id"]),kwargs)

def add_answer(**kwargs):
    answer=Answer(**kwargs)
    answer_id=get_next_answer_id()
    answer.id=answer_id
    #answer.addtime=datetime.now()
    load_answer_by_answer(answer)
    return answer_id

def delete_answer(question_id,answer_id):
    pass

def add_comment(**kwargs):
    comment=Comment(**kwargs)
    comment.id=get_next_comment_id()
    comment.addtime=datetime.now()
    load_comment_by_comment(comment)
    return comment.id

def delete_comment(answer_id,comment_id):
    pass

def favor_comment(answer_id,comment_id):
    pass

def cancel_favor_comment(commentevaluation_id):
    pass

