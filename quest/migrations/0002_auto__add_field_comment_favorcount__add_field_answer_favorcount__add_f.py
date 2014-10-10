# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Comment.favorcount'
        db.add_column(u'quest_comment', 'favorcount',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Answer.favorcount'
        db.add_column(u'quest_answer', 'favorcount',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Answer.opposecount'
        db.add_column(u'quest_answer', 'opposecount',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Question.user'
        db.add_column(u'quest_question', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['account.User']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Comment.favorcount'
        db.delete_column(u'quest_comment', 'favorcount')

        # Deleting field 'Answer.favorcount'
        db.delete_column(u'quest_answer', 'favorcount')

        # Deleting field 'Answer.opposecount'
        db.delete_column(u'quest_answer', 'opposecount')

        # Deleting field 'Question.user'
        db.delete_column(u'quest_question', 'user_id')


    models = {
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'addTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        u'quest.answer': {
            'Meta': {'object_name': 'Answer'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'commentcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'favorcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opposecount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quest.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'quest.answerevaluation': {
            'Meta': {'object_name': 'AnswerEvaluation'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quest.Answer']"}),
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'quest.comment': {
            'Meta': {'object_name': 'Comment'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quest.Answer']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'favorcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'touser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'tuser'", 'to': u"orm['account.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'fuser'", 'to': u"orm['account.User']"})
        },
        u'quest.commentevaluation': {
            'Comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quest.Comment']"}),
            'Meta': {'object_name': 'CommentEvaluation'},
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'quest.question': {
            'Meta': {'object_name': 'Question'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'answercount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['quest.Topic']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['account.User']"})
        },
        u'quest.topic': {
            'Meta': {'object_name': 'Topic'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        }
    }

    complete_apps = ['quest']