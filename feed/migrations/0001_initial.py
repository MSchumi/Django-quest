# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Activity'
        db.create_table(u'feed_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activitytype', self.gf('django.db.models.fields.IntegerField')()),
            ('contentid', self.gf('django.db.models.fields.IntegerField')()),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fromuser', to=orm['account.User'])),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='touser', to=orm['account.User'])),
            ('addtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'feed', ['Activity'])


    def backwards(self, orm):
        # Deleting model 'Activity'
        db.delete_table(u'feed_activity')


    models = {
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'addTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'friend': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['account.User']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        u'feed.activity': {
            'Meta': {'ordering': "['-addtime']", 'object_name': 'Activity'},
            'activitytype': ('django.db.models.fields.IntegerField', [], {}),
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'contentid': ('django.db.models.fields.IntegerField', [], {}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fromuser'", 'to': u"orm['account.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'touser'", 'to': u"orm['account.User']"})
        }
    }

    complete_apps = ['feed']