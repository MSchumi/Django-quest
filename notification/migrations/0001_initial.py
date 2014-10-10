# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table(u'notification_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('addtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message_type', self.gf('django.db.models.fields.IntegerField')()),
            ('contentid', self.gf('django.db.models.fields.IntegerField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mfuser', to=orm['account.User'])),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mtuser', to=orm['account.User'])),
        ))
        db.send_create_signal(u'notification', ['Message'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table(u'notification_message')


    models = {
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'addTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'follower': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ufollow'", 'symmetrical': 'False', 'through': u"orm['account.UserFollow']", 'to': u"orm['account.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        u'account.userfollow': {
            'Meta': {'object_name': 'UserFollow'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tuser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user'", 'to': u"orm['account.User']"}),
            'ufollow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_user'", 'to': u"orm['account.User']"})
        },
        u'notification.message': {
            'Meta': {'object_name': 'Message'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'contentid': ('django.db.models.fields.IntegerField', [], {}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mfuser'", 'to': u"orm['account.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_type': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mtuser'", 'to': u"orm['account.User']"})
        }
    }

    complete_apps = ['notification']