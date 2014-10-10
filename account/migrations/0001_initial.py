# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'account_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('addTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['User'])

        # Adding model 'Register_Temp'
        db.create_table(u'account_register_temp', (
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('activecode', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('addTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['Register_Temp'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'account_user')

        # Deleting model 'Register_Temp'
        db.delete_table(u'account_register_temp')


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