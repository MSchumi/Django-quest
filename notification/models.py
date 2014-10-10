#coding=utf-8
from django.db import models,connection
from account.models import User

class MessageManager(models.Manager):

    def bulk_insert_ignore(self,fields,value_list,print_sql=False):
        """主要解决mysql重复数据过滤的问题 加入了 ignore 关键词"""
        db_table = self.model._meta.db_table
        values_sql="(%s)" %(','.join([" %s " for _ in range(len(fields))]))
        base_sql = "INSERT IGNORE INTO %s (%s) VALUES " % (db_table, ",".join(fields))
        sql = """%s %s""" % (base_sql, values_sql)
        from django.db import connection,transaction
        cursor = connection.cursor()
        try:
            f=cursor.executemany(sql, value_list)
            k=transaction.commit_unless_managed()
            import pdb;pdb.set_trace()
            return True
        except Exception as e:
            print e
            return False

class Message(models.Model):
    op_type=(("add_answer",0),("follow_question",1),("evaluate_answer",2),("reply_answer",3),("reply_comment",4),("follow_user",5),)
    status=models.IntegerField()
    addtime=models.DateTimeField(auto_now_add=True)
    message_type=models.IntegerField()
    contentid=models.IntegerField()
    content=models.TextField()
    from_user=models.ForeignKey(User,related_name='mfuser')
    to_user=models.ForeignKey(User,related_name='mtuser')
    objects=models.Manager()
    messageobjects=MessageManager()

    class Meta:
        unique_together = ('contentid', 'message_type','to_user')
        ordering=["-addtime"]
