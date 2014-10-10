#coding:utf-8
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template import loader
from django.conf import settings 
import traceback

def send_confirmemail(email=None,activecode=None,username=None):
    subject,from_email,to=u'来自Formula One的注册确认邮件',u'msliudongsheng@163.com',email
    text_content='This is an important message'
    address=settings.QUESTION_RUL
    active_address=address+u'/account/confirm/'+activecode+'/'
    html_content=loader.render_to_string('email/email_confirm.html',{'address':address,'name':username,'active_address':active_address})
    msg=EmailMultiAlternatives(subject,text_content,from_email,(to,))
    msg.attach_alternative(html_content,'text/html')
    msg.send()
