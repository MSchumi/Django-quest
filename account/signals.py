#coding=utf-8
import django.dispatch

register_user_done=django.dispatch.Signal(providing_args=['instance'])
follow_user_done=django.dispatch.Signal(providing_args=['fuser','tuser','optype',"follow_id"])
