#coding=utf-8
import json
from django.conf import settings 

import pysolr

from quest.models import Question,Answer
from account.models import User

from quest.signals import  question_submit_done,answer_submit_done,vote_submit_done,follow_question_done
from account.signals import register_user_done

class QSolr(object):
    "实现solr的检索、搜索建议、增加、删除"
    __solr_url=settings.SOLR_URL
    def __init__(self,core_name=None,wt='json'):
        self.core_name=core_name
        if core_name:
            self.__solr=pysolr.Solr(self.__solr_url+core_name)
        if wt:
            self.wt=wt
    def search(self,field=None,keyword=None,rflist=None,start=0,rows=10,hlfield=None):
        search_str=keyword
        search_param_dict=dict({'wt':self.wt})
        if field and keyword:
            search_str=field+":"+keyword
        else:
            return None

        if rflist:
            search_param_dict['fl']=','.join(rflist)
        if rows:
            search_param_dict['start']=start
            search_param_dict['rows']=rows
        if hlfield:
            search_param_dict['hl']='true'
            search_param_dict['hl.fl']=hlfield
            search_param_dict['hl.simple.pre']='<em>'
            search_param_dict['hl.simple.post']='</em>'  
        results=self.__solr.search(search_str,**search_param_dict)
        return results

    def suggestion(self,field=None,keyword=None,rflist=None,start=0,rows=10,hlfield=None): 
        results=self.search(field,keyword,rflist,start=0,rows=10,hlfield=hlfield)
        if results: 
            if results.hits:
                if not hlfield:
                    return results.docs
                else:
                    self.changeResult(results)
                    return results.docs
        return None

    def add(self,dic_list):
        "保存数据到solr 字段以字典形式传递"
        try:
            self.__solr.add(dic_list)
            return True
        except:
            return False
    def remove(self,field,value):
        self.__solr.remove(field=value)
        
    def changeresult(self,results,field):
        highlighting=results.highlighting
        for doc in results.docs:
            doc[field]=highlighting[doc['id']][field]
        return results

    def combineresult(self,field,result,objects_list):
        #import pdb;pdb.set_trace()
        if objects_list:
            for obj in objects_list:
                for doc in result.docs:
                    if doc['id']==str(obj.id):
                        setattr(obj,field,doc[field][0])
                        break
        return objects_list


class QuestionSolr(QSolr):
    def __init__(self):
        super(QuestionSolr,self).__init__(settings.QUESTION_CORE)

    def suggestion(self,word):
        return super(QuestionSolr,self).suggestion(field='title',keyword=word,rflist=('title','id'))

    def search_by_keyword(self,q):
        results=super(QuestionSolr,self).search(field='title',keyword=q,rflist=('title','id'),hlfield='title')
        results=super(QuestionSolr,self).changeresult(results,field='title')
        id_list=[doc['id'] for doc in results.docs ]
        question_list=Question.questionobjects.get_questions_by_id(id_list)
        return self.combineresult('title',results,question_list)

    def add(self,question):
        solr_dict={'id':question.id,'title':question.title,'userid':question.user_id}
        return super(QuestionSolr,self).add([solr_dict])

    def remove(self,question_id):
        return super(QuestionSolr,self).remove('id',question_id)




class AnswerSolr(QSolr):
    def __init__(self):
        super(AnswerSolr,self).__init__(settings.ANSWER_CORE)

    def search_by_keyword(self,q):
        results=super(AnswerSolr,self).search(field='content',keyword=q,rflist=('content','id'),hlfield='content')
        results=super(AnswerSolr,self).changeresult(results,field='content')
        id_list=[doc['id'] for doc in results.docs]
        answer_list=Answer.objects.select_related('question,user').filter(pk__in=id_list)
        return self.combineresult('content',results,answer_list)

    def add(self,answer):
        solr_dict={'id':answer.id,'content':answer.content,'userid':answer.user_id,'questionid':answer.question_id}
        return super(AnswerSolr,self).add([solr_dict])

    def remove(self,answer_id):
        return super(AnswerSolr,self).remove('id',answer_id)

class UserSolr(QSolr):
    def __init__(self):
        super(UserSolr,self).__init__(settings.USER_CORE)

    def suggestion(self,word):
        return super(UserSolr,self).suggestion(field='username',keyword=word,rflist=('username','id','avatar'))

    def search_by_keyword(self,q):
        results=super(UserSolr,self).search(field='username',keyword=q,rflist=('username','id'),hlfield='username')
        results=super(UserSolr,self).changeresult(results,field='username')
        id_list=[doc['id'] for doc in results.docs]
        user_list=User.objects.filter(pk__in=id_list)
        return self.combineresult('username',results,user_list)

    def add(self,user):
        solr_dict={'id':user.id,'username':user.surname+user.name}
        return super(UserSolr,self).add([solr_dict])

    def remove(self,user_id):
        return super(UserSolr,self).remove('id',user_id)








