#encoding=utf-8
from datetime import datetime,timedelta
from django.template import Library
from django import template
from django.template.loader import render_to_string

register =Library()

@register.filter
def messagetype(value,arg):
    if value==1:
        return u"回答了问题"
    elif value==2:
        return u"关注了问题"
    elif value==3:
        if not arg["status"]:
            return ""
        if int(arg["status"])==1:
            return u"赞了回答"
        else:
            return u"反对了回答"
    elif value==4:
        return u"评论了回答"
    elif value==5:
        return u'回复了评论'
    elif value==6:
        return u'关注了你'
    else:
        return ""
@register.filter
def messagecontent(value):
    
    if value["status"]:
        return get_read_message_html(value)
    else:
        return get_unread_message_html(value)
   
def get_unread_message_html(value):
    html_str=""
    message_type=value["message_type"]
    content=value["content"]
    if message_type==1:
        html_str="<a href='/notification/read/?m="+str(value["message_type"])+"&c="+str(value["content_id"])+"&f="+str(value["fuser_id"])+"&a=/question/"+str(content['question_id'])+"/?answerid="+str(content['answer_id'])+"'>"+content["question_title"]+"</a>"
    elif message_type==2:
        html_str="<a href='/notification/read/?m="+str(value["message_type"])+"&c="+str(value["content_id"])+"&f="+str(value["fuser_id"])+"&a=/question/"+str(content['question_id'])+"'>"+content["question_title"]+"</a>"
    elif message_type==3:
        html_str="<a href='/notification/read/?m="+str(value["message_type"])+"&c="+str(value["content_id"])+"&f="+str(value["fuser_id"])+"&a=/question/"+str(content['question_id'])+"#"+str(content['answer_id'])+"'>"+content["answer_content"]+"</a>"
    elif message_type==4 or message_type==5:
        html_str="<a href='/notification/read/?m="+str(value["message_type"])+"&c="+str(value["content_id"])+"&f="+str(value["fuser_id"])+"&a=/question/"+str(content['question_id'])+"#"+str(content['answer_id'])+"#"+str(content['comment_id'])+"'>"+content["answer_content"]+"</a>"
    else:
        html_str=""
    return html_str


def get_read_message_html(value):
    html_str=""
    message_type=value["message_type"]
    content=value["content"]
    if message_type==1:
        html_str="<a href='/question/"+str(content['question_id'])+"/?answerid="+str(content['answer_id'])+"'>"+content["question_title"]+"</a>"
    elif message_type==2:
        html_str="<a href='/question/"+str(content['question_id'])+"'>"+content["question_title"]+"</a>"
    elif message_type==3:
        html_str="<a href='/question/"+str(content['question_id'])+"#"+str(content['answer_id'])+"'>"+content["answer_content"]+"</a>"
    elif message_type==4 or message_type==5:
        html_str="<a href='/question/"+str(content['question_id'])+"#"+str(content['answer_id'])+"#"+str(content['comment_id'])+"'>"+content["answer_content"]+"</a>"
    else:
        html_str=""
    return html_str
    
        

