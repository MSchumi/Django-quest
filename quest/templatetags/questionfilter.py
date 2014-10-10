#encoding=utf-8
from django.template import Library
import re
register =Library()

@register.filter(name='contains')
def contains(value,arg):
    return arg in value

@register.filter(name='summarize')
def summarize(value,arg):
    if value:
        pattern=re.compile(r'<.*?>')
        value=pattern.sub("",value,0)
        return value[:arg]
    else:
        return ""
@register.filter(name="noneto0")
def noneto0(value):
    if not value:
        return 0
    return value
@register.filter(name="convertnum")
def convertnum(value):
    if value:
        return value
    else:
        return 0

@register.filter(name="convertempty")
def convertempty(value):
    if value:
        return value
    else:
        return ""

