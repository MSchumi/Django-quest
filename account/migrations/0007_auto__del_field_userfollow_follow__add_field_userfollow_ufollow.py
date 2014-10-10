# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserFollow.follow'
        db.delete_column(u'account_userfollow', 'follow_id')

        # Adding field 'UserFollow.ufollow'
        db.add_column(u'account_userfollow', 'ufollow',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='from_user', to=orm['account.User']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'UserFollow.follow'
        db.add_column(u'account_userfollow', 'follow',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, related_name='from_user', to=orm['account.User']),
                      keep_default=False)

        # Deleting field 'UserFollow.ufollow'
        db.delete_column(u'account_userfollow', 'ufollow_id')


    models = {
        u'account.register_temp': {
            'Meta': {'object_name': 'Register_Temp'},
            'activecode': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'addTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'addTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'follower': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'userfollow'", 'symmetrical': 'False', 'through': u"orm['account.UserFollow']", 'to': u"orm['account.User']"}),
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
        }
    }

    complete_apps = ['account']