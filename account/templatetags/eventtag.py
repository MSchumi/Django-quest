#encoding=utf-8
from datetime import datetime,timedelta
from django.template import Library
from django import template
from django.template.loader import render_to_string
from quest.models import Question,Answer

register =Library()

@register.filter(name='contains')
def contains(value,arg):
    return arg in value
@register.filter(name="eventtime")
def eventtime(value):
    now=datetime.now()
    delta=now-value.replace(tzinfo=None)
    if delta.days:
        if delta.days/360>0:
            return str(delta.days/360)+"年前"
        elif delta.days/30>0:
            return str(delta.days/30)+"月前"
        elif delta.days/7>0:
            return str(delta.days/7)+"周前"
        else:
            return str(delta.days)+"天前"
    else:
        if delta.seconds/3600>0:
            return str(delta.seconds/3600)+"小时前"
        elif delta.seconds/60>0:
            return str(delta.seconds/60)+"分钟前"
        else:
            return str(delta.seconds)+"秒前"
@register.filter
def eventtype(value,arg):
    if value==0:
        return u"提了问题"
    elif value==1:
        return u"回答了问题"
    elif value==2:
        return u"关注了问题"
    elif value==3:
        if arg.status==1:
            return u"赞了回答"
        else:
            return u"反对了回答"
    elif value==4:
        return u"关注了话题"

class EventNode(template.Node):
    def __init__(self,sequence):
        self.sequence=sequence
    def answer_render(self,data,user=None):
        html_str=render_to_string('answer.html',{'answer':data,'user':user})
        return html_str
    def evaluate_render(self,data,user=None):
        html_str=render_to_string('answer_evaluation.html',{'evaluation':data,'user':user})
        return html_str
    def question_render(self,data,user=None):
        html_str=render_to_string('uquestion.html',{'question':data,'user':user})
        return html_str
    def follow_render(self,data,user=None):
        html_str=render_to_string('uquestion.html',{'question':data.question,'user':user})
        return html_str
    def render(self,context):
        event=context['event']
        user=context['user']
        values = self.sequence.resolve(context, True)
        if event["eventtype"]==0:
            return self.question_render(event["data"],user)
        elif event["eventtype"]==1 :
            return self.answer_render(event["data"],user)
        elif event["eventtype"]==2:
            return self.follow_render(event["data"],user)
        elif event["eventtype"]==3:
            return self.evaluate_render(event["data"],user)
        else:
            return ""
        return self.event

@register.simple_tag
def event(data):
    try:
        tag_name,event=token.split_contents()
        return "test1"
    except Exception,e:
        return  "test"

@register.tag(name="event_html")
def event_html(parser,token):
    try:
        tag_name,event=token.split_contents()
        sequence=parser.compile_filter(event)
    except ValueError:
        raise template.TemplateSyntaxError("parse error")
    return EventNode(sequence)


