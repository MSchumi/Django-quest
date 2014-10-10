# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserFollow'
        db.create_table(u'account_userfollow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('follow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_user', to=orm['account.User'])),
            ('tuser', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_user', to=orm['account.User'])),
            ('addtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['UserFollow'])

        # Removing M2M table for field friend on 'User'
        db.delete_table(db.shorten_name(u'account_user_friend'))


    def backwards(self, orm):
        # Deleting model 'UserFollow'
        db.delete_table(u'account_userfollow')

        # Adding M2M table for field friend on 'User'
        m2m_table_name = db.shorten_name(u'account_user_friend')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_user', models.ForeignKey(orm[u'account.user'], null=False)),
            ('to_user', models.ForeignKey(orm[u'account.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_user_id', 'to_user_id'])


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
            'friend': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['account.User']", 'through': u"orm['account.UserFollow']", 'symmetrical': 'False'}),
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
            'follow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_user'", 'to': u"orm['account.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tuser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user'", 'to': u"orm['account.User']"})
        }
    }

    complete_apps = ['account']