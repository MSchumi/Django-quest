#coding=utf-8
from  django.template import Library
from django import template
from django.template.loader import render_to_string
from quest.models import Question,Answer

register=Library()
@register.tag
def activity_html(parser,token):
    try:
        tag_name,activity=token.split_contents()
        sequence=parser.compile_filter(activity)
    except ValueError:
        raise template.TemplateSyntaxError("parse error")
    return ActivityNode(sequence)
class ActivityNode(template.Node):
    "用于不同好友动态页面的处理"
    def __init__(self,sequence):
        self.sequence=sequence
    def render(self,context):
        import pdb;pdb.set_trace()
        activity=context['activity']
        if activity["activitytype"]==0:
            return self.question_render(activity["data"],activity["fuser"],activity)
        elif activity["activitytype"]==1 :
            return self.answer_render(activity["data"],activity["fuser"],activity)
        elif activity["activitytype"]==2:
            return self.follow_render(activity["data"],activity["fuser"],activity)
        elif activity["activitytype"]==3:
            return self.evaluate_render(activity["data"],activity["fuser"],activity)
        else:
            return ""

    def answer_render(self,data,user,activity):
        html_str=render_to_string('activity_answer.html',{'answer':data,'fuser':user,"activity":activity})
        return html_str

    def evaluate_render(self,data,user,activity):
        html_str=render_to_string('activity_answer_evaluation.html',{'evaluation':data,'fuser':user,"activity":activity})
        return html_str

    def question_render(self,data,user,activity):
        html_str=render_to_string('activity_question.html',{'question':data,'fuser':user,"activity":activity})
        return html_str

    def follow_render(self,data,user,activity):
        html_str=render_to_string('activity_question.html',{'question':data.question,'fuser':user,"activity":activity})
        return html_st
