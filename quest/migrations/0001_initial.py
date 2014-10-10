# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Topic'
        db.create_table(u'quest_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('addtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edittime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'quest', ['Topic'])

        # Adding model 'Question'
        db.create_table(u'quest_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('addtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edittime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('answercount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'quest', ['Question'])

        # Adding M2M table for field topics on 'Question'
        m2m_table_name = db.shorten_name(u'quest_question_topics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'quest.question'], null=False)),
            ('topic', models.ForeignKey(orm[u'quest.topic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'topic_id'])

        # Adding model 'Answer'
        db.create_table(u'quest_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quest.Question'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('addtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edittime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('commentcount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'quest', ['Answer'])

        # Adding model 'Comment'
        db.create_table(u'quest_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quest.Answer'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'fromuser', to=orm['account.User'])),
            ('touser', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'touser', to=orm['account.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('addtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edittime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'quest', ['Comment'])

        # Adding model 'AnswerEvaluation'
        db.create_table(u'quest_answerevaluation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quest.Answer'])),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('edittime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'quest', ['AnswerEvaluation'])

        # Adding model 'CommentEvaluation'
        db.create_table(u'quest_commentevaluation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('Comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quest.Comment'])),
            ('edittime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'quest', ['CommentEvaluation'])


    def backwards(self, orm):
        # Deleting model 'Topic'
        db.delete_table(u'quest_topic')

        # Deleting model 'Question'
        db.delete_table(u'quest_question')

        # Removing M2M table for field topics on 'Question'
        db.delete_table(db.shorten_name(u'quest_question_topics'))

        # Deleting model 'Answer'
        db.delete_table(u'quest_answer')

        # Deleting model 'Comment'
        db.delete_table(u'quest_comment')

        # Deleting model 'AnswerEvaluation'
        db.delete_table(u'quest_answerevaluation')

        # Deleting model 'CommentEvaluation'
        db.delete_table(u'quest_commentevaluation')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'touser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'touser'", 'to': u"orm['account.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'fromuser'", 'to': u"orm['account.User']"})
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
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['quest.Topic']", 'symmetrical': 'False'})
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