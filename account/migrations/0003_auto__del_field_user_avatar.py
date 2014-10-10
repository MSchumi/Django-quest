# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'User.avatar'
        db.delete_column(u'account_user', 'avatar')


    def backwards(self, orm):
        # Adding field 'User.avatar'
        db.add_column(u'account_user', 'avatar',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100),
                      keep_default=False)


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
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        }
    }

    complete_apps = ['account']