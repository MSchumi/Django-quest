#coding=utf-8
from redishelper.question import add_answer,get_question_from_redis,update_question,evaluate_answer,update_answer,add_comment,submit_question,\
        get_answer_by_answer_id
from quest.models import Answer,Question
from redishelper.timeline_util import follow_question,cancle_follow_question

def add_answer_to_redis(**kwargs):
    answer_id=add_answer(**kwargs)
    question_id=kwargs["question_id"]
    #import pdb;pdb.set_trace()
    question=get_question_from_redis(question_id)
    question.answercount+=1
    update_question(question_id,answercount=int(question.answercount))
    Question.objects.filter(pk=int(question_id)).update(answercount=int(question.answercount))
    return answer_id

def add_comment_to_redis(**kwargs):
    comment_id=add_comment(**kwargs)
    comment_id=add_comment(**kwargs)
    answer=get_answer_by_answer_id(kwargs["answer_id"])
    answer.commentcount+=1
    #import pdb;pdb.set_trace()
    update_answer(id=answer.id,commentcount=answer.commentcount)
    Answer.objects.filter(pk=answer.id).update(commentcount=answer.commentcount)

def add_question_to_redis(**kwargs):
    question_id=submit_question(**kwargs)
    return question_id


def update_answer_to_redis(**kwargs):
    comment_id=add_comment(**kwargs)
    answer_id=kwargs["answer_id"]  
    answer=get_answer_by_answer_id(answer_id)
    answer.commentcount+=1
    update_answer(answer.id,commentcount=answer.commentcount)
    answer.save()
    return comment_id
 
def submit_vote_to_redis(user,answer_id,status,evaluation_id=None):
    answer=get_answer_by_answer_id(answer_id)
    evaluate_answer(answer_id,user.id,status,evaluation_id=evaluation_id)
    is_exists=False
    #import pdb;pdb.set_trace()
    if evaluation_id and evaluation_id!=0:
        is_exists=True
    if status==1:
        if is_exists:
            answer.opposecount-=1
        answer.favorcount+=1
    else:
        if is_exists:
            answer.favorcount-=1
        answer.opposecount+=1
    update_answer(id=answer.id,favorcount=answer.favorcount,opposecount=answer.opposecount)
    Answer.objects.filter(pk=answer_id).update(favorcount=answer.favorcount,opposecount=answer.opposecount)
    return True

def cancel_vote_to_redis(user,answer_id,status,evaluation_id):
    evaluate_answer(answer_id,user.id,status,evaluation_id=evaluation_id,cancel=True)
    answer=get_answer_by_answer_id(answer_id)
    if status==1:
        answer.favorcount-=1
    else:
        answer.opposecount-=1 
    update_answer(id=answer_id,favorcount=answer.favorcount,opposecount=answer.opposecount)
    #import pdb;pdb.set_trace()
    Answer.objects.filter(pk=answer_id).update(favorcount=answer.favorcount,opposecount=answer.opposecount) 
    return True

def follow_question_to_redis(question_id,user_id):
    follow_question(question_id,user_id)

def cancel_follow_question_to_redis(question_id,user_id):
    cancle_follow_question(question_id,user_id)
