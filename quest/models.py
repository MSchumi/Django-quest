#coding=utf-8
import copy

from django.db import models,connection
from django.core.urlresolvers import reverse
from quest.signals import save_activity,question_submit_done,answer_submit_done,vote_submit_done,follow_question_done,comment_submit_done
from account.models import User


class AnswerManager(models.Manager):
    """还为将大sql改为存储过程 
    """
    def get_answerlist(self,qid=None,uid=None):
        """ get answers list width user evaluation by question_id and user_id
        """
        if qid:
            answer_list=[]
            cursor=connection.cursor()
            if uid:
                cursor.execute("""
                select a.id,a.content,a.addtime,a.commentcount,a.favorcount,a.opposecount,u.id uid,u.email,u.name,u.surname,
                e.status,e.evaluation_id as eid,u.avatar avatar from quest_answer a inner join account_user u on a.user_id=u.id left join\
                quest_answerevaluation e on (a.id=e.answer_id and e.user_id=%s ) where a.question_id=%s 
                """,[uid,qid])
            else:
                cursor.execute("""
                select a.id,a.content,a.addtime,a.commentcount,a.favorcount,a.opposecount,u.id uid,u.email,u.name,u.surname,
                null as status,null as eid,u.avatar avatar from quest_answer a inner join account_user u on a.user_id=u.id 
                where a.question_id=%s""",[qid])
            for row in cursor.fetchall():
                answer=self.model(id=row[0],content=row[1],addtime=row[2],commentcount=row[3],favorcount=row[4],\
                        opposecount=row[5],user=User(id=row[6],email=row[7],name=row[8],surname=row[9],avatar=row[12]),\
                        question=Question(id=qid))
                answer.evaluation=row[10]
                #import pdb;pdb.set_trace()
                if not row[10]:
                    answer.evaluation=0
                    answer.eid=row[11]
                answer_list.append(answer)
            return answer_list
        else:
            return None
    def create(self,answer_id,**kwargs):
        "添加redis缓存,同时获取id"
        answer=super(AnswerManager,self).create(id=answer_id,**kwargs)
        answer_submit_done.send(sender=Answer,obj=answer,user=kwargs.get("user"),question=kwargs.get("question"))
        return answer


class QuestionManager(models.Manager):
    
    def get_questions(self):
        question_list=[]
        cursor=connection.cursor()
        cursor.execute("""
        select q.id,q.title,q.addtime,u.id,u.`name`,u.surname,u.avatar ,a.aid,a.qacontent,a.qafcount,a.qapcount,
        a.qacommentcount,a.qatime,a.buid,a.buname,a.busurname,a.buavatar from quest_question q LEFT JOIN account_user u on
        u.id=q.user_id LEFT JOIN (select question_id, qa.id as aid,qa.content as qacontent,qa.favorcount as qafcount,
        qa.opposecount as qapcount, qa.addtime as qatime,qa.commentcount qacommentcount,bu.id buid,bu.name buname,bu.surname 
        busurname,bu.avatar buavatar from quest_answer qa  LEFT JOIN account_user bu on qa.user_id=bu.id  where qa.id=(SELECT 
        id  from quest_answer qa1 where qa.question_id=qa1.question_id ORDER BY favorcount DESC limit 1))a on q.id=
        a.question_id ORDER BY answercount DESC limit 10 """)
        #import pdb;pdb.set_trace()
        for row in cursor.fetchall():
            question=self.model(id=row[0],title=row[1],addtime=row[2],user=User(id=row[3],name=row[4],surname=row[5],\
            avatar=row[6]))
            question.answer=Answer(id=row[7],content=row[8],favorcount=row[9],opposecount=row[10],commentcount=row[11],\
            addtime=row[12])
            question.answer.user=User(id=row[13],name=row[14],surname=row[15],avatar=row[16])
            question_list.append(question)
        return question_list
    
    def get_questions_by_id(self,id_list):
        question_list=[]
        if id_list:
            cursor=connection.cursor()
            #import pdb;pdb.set_trace()
            cursor.execute("""select q.id as qid, q.title as qtitle,q.answercount as answercount,aid,acontent,uid ,`name`,surname
            ,avatar,followcount from quest_question q left join (select a.id as aid,a.question_id as question_id, a.content
            as acontent, au.id as uid ,au.`name` as `name`, au.surname as surname ,au.avatar as avatar from quest_answer
            a left JOIN account_user au on a.user_id=au.id  WHERE a.id=(select id from quest_answer a1 where
            a1.question_id=a.question_id ORDER BY a1.favorcount desc limit 1 ))a2 on a2.question_id=q.id left join ( select
            COUNT(question_id) as followcount,question_id  from quest_qustionfollow GROUP BY question_id)qf on
            qf.question_id=q.id where q.id in("""+','.join(['%s' for _ in id_list])+")",id_list)
            for row in cursor.fetchall():
                question=self.model(id=row[0],title=row[1],answercount=row[2])
                if row[3]:
                    question.answer=Answer(id=row[3],content=row[4],user=User(id=row[5],name=row[6],surname=row[7],avatar=row[8]))
                if not row[9]:
                    question.followcount=0
                question_list.append(question)
        return question_list

    def create(self,**kwargs):
        #import pdb;pdb.set_trace()
        question=super(QuestionManager,self).create(**kwargs)
        question_submit_done.send(sender=Question,obj=question,user=kwargs["user"])
        return question

class Topic(models.Model):
    user=models.ForeignKey(User)
    title=models.CharField(max_length=200)
    addtime=models.DateTimeField(auto_now_add=True)
    edittime=models.DateTimeField(auto_now=True,null=True)
    
    def __unicode__(self):
        return self.title


class Question(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    category=models.CharField(max_length=200,null=True)
    addtime=models.DateTimeField(auto_now_add=True)
    edittime=models.DateTimeField(auto_now=True,null=True)
    answercount=models.IntegerField(u'回答数量',default=0)
    topics=models.ManyToManyField(Topic)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    browsecount=models.IntegerField(default=0)
    follower=models.ManyToManyField(User,related_name="questions",through="QustionFollow")
    objects=models.Manager()
    questionobjects=QuestionManager()

    def __unicode__(self):
        return self.title
    def submit_question(self,user):
        if self.title!="":
            self.save()
            question_submit_done.send(sender=Question,obj=self,user=user)
        else:
            return None
        return self.id

    def get_absolute_url(self):
        #import pdb;pdb.set_trace()
        return reverse("question_detail",args=[self.id])

class QuestionFollowManager(models.Manager):
    def create(**kwargs):
        instance=super(QuestionFollowManager,self).create(**kwargs)
        follow_question_done.send(sender=QustionFollow,instance=instance,user=kwargs["user"],optype="save")
        return insatnce

    def create(**kwargs):
        instance=super(QuestionFollowManager,self).create(**kwargs)
        follow_question_done.send(sender=QustionFollow,instance=instance.id,user=user,optype="delete")
        instance.delete()

class QustionFollow(models.Model):
    user=models.ForeignKey(User)
    question=models.ForeignKey(Question)
    addtime=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    questionfollowobjects=QuestionFollowManager()

    def __unicode__(self):
        return self.addtime

    def follow_question(self,user):
        self.save()
        follow_question_done.send(sender=QustionFollow,instance=self,user=user,optype="save")

    def cancel_follow(self,user):
        follow_question_done.send(sender=QustionFollow,instance=self.question.id,user=user,optype="delete")#对于关注问题 contentid 为问题id
        self.delete()

class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    addtime=models.DateTimeField(auto_now_add=True)
    edittime=models.DateTimeField(auto_now=True,null=True)
    commentcount=models.IntegerField(u'评论数量',default=0)
    favorcount=models.IntegerField(u'赞的数量',default=0)
    opposecount=models.IntegerField(u'反对的数量',default=0)
    answerobjects=AnswerManager()
    objects = models.Manager()

    def __uincode__(self):
        return self.content

    def submit_answer(self,user):
        add_answer(self)
        self.save()
        question=Question.objects.get(pk=self.question_id)
        question.answercount+=1
        question.save()
        answer_submit_done.send(sender=Answer,obj=self,user=user,question=question)
        return self.id
    
    class Meta:
        ordering=["addtime"]
     
class CommentManager(models.Manager):
    def create(self,**kwargs):
        comment=super(CommentManager,self).create(**kwargs)
        if comment.answer.user.id==comment.touser_id:
            comment_submit_done.send(sender=Comment,instance=comment,user=comment.user,commenttype=0,optype="save")#回复答案
        else:
            comment_submit_done.send(sender=Comment,instance=comment,user=comment.user,commenttype=1,optype="save")#回复评论
        return comment


class Comment(models.Model):
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name=u'fuser',on_delete=models.CASCADE,related_query_name="fuser")
    touser=models.ForeignKey(User,related_name=u'tuser',on_delete=models.CASCADE,related_query_name="tuser")
    content=models.TextField()
    addtime=models.DateTimeField(auto_now_add=True)
    edittime=models.DateTimeField(auto_now=True,null=True)
    favorcount=models.IntegerField(u'赞的数量',default=0)
    commentobjects=CommentManager()
    objects=models.Manager()

    def __unicode__(self):
        return self.content
    def submit_comment(self):
        pass

    class Meta:
        ordering=["addtime"]


class AnswerEvaluationManager(models.Manager):
    def submit_voter(self,user,answer,status,evaluation_id=None):
        instance=self.model(user=user,answer=answer,status=status)
        if evaluation_id or evaluation_id==0:
            instance.id=evaluation_id
        instance.save()
        vote_submit_done.send(sender=AnswerEvaluation,instance=instance,user=user,optype="save")
        return instance.id

    def cancel_vote(self,user,answer,status,evaluation_id):
        instance=self.model(id=evaluation_id,answer=answer,user=user)
        instance.delete()
        vote_submit_done.send(sender=AnswerEvaluation,instance=instance.id,user=user,optype="delete")




class AnswerEvaluation(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    status=models.IntegerField(u'状态')
    edittime=models.DateTimeField(auto_now=True,null=True)
    objects=models.Manager()
    evaluationobjects=AnswerEvaluationManager()

    def __unicode__(self):
        return self.status

    def submit_vote(self,user,status,is_exists):
        self.status=status
        self.save()
        if status==1:
            if is_exists:
                self.answer.opposecount-=1
            self.answer.favorcount+=1
            self.answer.save()
        else:
            if is_exists:
                 self.answer.favorcount-=1
            self.answer.opposecount+=1
            self.answer.save()
        vote_submit_done.send(sender=AnswerEvaluation,instance=self,user=user,optype="save")

    def cancel_vote(self,user,status):
        if status==1:
            self.answer.favorcount-=1
            self.answer.save()
        else:
            self.answer.opposecount-=1
            self.answer.save()

        vote_submit_done.send(sender=AnswerEvaluation,instance=self.id,user=user,optype="delete")
        self.delete()
        

    
class CommentEvaluation(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Comment=models.ForeignKey(Comment)
    edittime=models.DateTimeField(auto_now=True,null=True)


class EventManger(models.Manager):
    def get_event_list(self,userid,**kwargs):
        event_list=[]
        question_submit_count=0
        answer_count=0
        page=kwargs.pop('page',1)
        pagecount=kwargs.pop('pagecount',15)
        cursor=connection.cursor()
        cursor.callproc("sp_userevent",(userid,(page-1)*15,pagecount))
        for row in cursor.fetchall():
            if row[0]==0:
                question=Question(id=row[13],title=row[14])
                user=User(id=row[15],name=row[16],surname=row[17],avatar=row[18])
                question.user=user
                event_list.append({'eventtype':row[0],'addtime':row[1],"data":question})
                question_submit_count+=1
            elif row[0]==1:
                answer=Answer(id=row[3],content=row[4],addtime=row[5],commentcount=row[6],favorcount=row[7],opposecount=row[8])
                answer.user=User(id=row[9],name=row[10],surname=row[11],avatar=row[12])
                answer.question=Question(id=row[13],title=row[14],user=User(id=row[15],name=row[16],surname=row[17],avatar=row[18])) 
                event_list.append({'eventtype':row[0],'addtime':row[1],"data":answer})
                answer_count +=1
            elif row[0]==2:
                follow=QustionFollow(id=row[19])
                question=Question(id=row[13],title=row[14])
                user=User(id=row[15],name=row[16],surname=row[17],avatar=row[18])
                question.user=user
                follow.question=question
                event_list.append({'eventtype':row[0],'addtime':row[1],"data":follow})
            elif row[0]==3:
                evalue=AnswerEvaluation(status=row[2])
                answer=Answer(id=row[3],content=row[4],addtime=row[5],commentcount=row[6],favorcount=row[7],opposecount=row[8])
                answer.user=User(id=row[9],name=row[10],surname=row[11],avatar=row[12])
                answer.question=Question(id=row[13],title=row[14],user=User(id=row[15],name=row[16],surname=row[17],avatar=row[18]))
                evalue.answer=answer
                event_list.append({'eventtype':row[0],'addtime':row[1],"data":evalue})
            
        return {"event_list":event_list,"statistics":{"submit_question":question_submit_count,"answer":answer_count}}
    def get_events(self,user_id):
        instances=self.model.objects.filter(user_id=user_id)
        return instances

class Event(models.Model):
    op_type=(("submit_question",0),("add_answer",1),("follow_question",2),("evaluate_answer",3),("follow_topic",4),)
    user=models.ForeignKey(User)
    #content=models.TextField()
    eventtype=models.IntegerField(choices=op_type)
    contentid=models.IntegerField()
    addtime=models.DateTimeField(auto_now_add=True)
    isdelete=models.BooleanField(default=False)
    objects=models.Manager()
    eventobjects=EventManger()

    class Meta:
        ordering = ['-addtime']
        #unique_together=("eventtype","contentid")

class EventContent(models.Model):
    event=models.OneToOneField(Event)
    content=models.TextField()
    addtime=models.DateTimeField(auto_now_add=True)







