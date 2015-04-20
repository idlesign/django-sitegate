# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Preferences'
        db.delete_table(u'sitegate_preferences')


        # Changing field 'EmailConfirmation.user'
        db.alter_column(u'sitegate_emailconfirmation', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'InvitationCode.creator'
        db.alter_column(u'sitegate_invitationcode', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'InvitationCode.acceptor'
        db.alter_column(u'sitegate_invitationcode', 'acceptor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

    def backwards(self, orm):
        # Adding model 'Preferences'
        db.create_table(u'sitegate_preferences', (
            ('signup_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('signin_disabled_text', self.gf('django.db.models.fields.TextField')(default='Sign in is disabled.')),
            ('signup_verify_email_body', self.gf('django.db.models.fields.TextField')(default='Please follow the link below to activate your account:\n%(link)s')),
            ('signup_verify_email_title', self.gf('django.db.models.fields.CharField')(default='Account activation', max_length=160)),
            ('signin_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signup_disabled_text', self.gf('django.db.models.fields.TextField')(default='Sign up is disabled.')),
        ))
        db.send_create_signal('sitegate', ['Preferences'])


        # Changing field 'EmailConfirmation.user'
        db.alter_column(u'sitegate_emailconfirmation', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.User']))

        # Changing field 'InvitationCode.creator'
        db.alter_column(u'sitegate_invitationcode', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.User']))

        # Changing field 'InvitationCode.acceptor'
        db.alter_column(u'sitegate_invitationcode', 'acceptor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['apps.User']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sitegate.blacklisteddomain': {
            'Meta': {'object_name': 'BlacklistedDomain'},
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '253'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sitegate.emailconfirmation': {
            'Meta': {'object_name': 'EmailConfirmation'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'expired': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_accepted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'sitegate.invitationcode': {
            'Meta': {'object_name': 'InvitationCode'},
            'acceptor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'acceptors'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creators'", 'to': u"orm['auth.User']"}),
            'expired': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_accepted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sitegate']