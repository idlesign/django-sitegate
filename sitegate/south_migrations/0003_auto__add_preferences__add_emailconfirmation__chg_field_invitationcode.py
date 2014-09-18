# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Preferences'
        db.create_table('sitegate_preferences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signin_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('signin_disabled_text', self.gf('django.db.models.fields.TextField')(default='Sign in is disabled.')),
            ('signup_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('signup_disabled_text', self.gf('django.db.models.fields.TextField')(default='Sign up is disabled.')),
            ('signup_verify_email_title', self.gf('django.db.models.fields.CharField')(max_length=160, default='Account activation')),
            ('signup_verify_email_body', self.gf('django.db.models.fields.TextField')(default='Please follow the link below to activate your account:\n%(link)s')),
        ))
        db.send_create_signal('sitegate', ['Preferences'])

        # Adding model 'EmailConfirmation'
        db.create_table('sitegate_emailconfirmation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_accepted', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('expired', self.gf('django.db.models.fields.BooleanField')(db_index=True, default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.User'])),
        ))
        db.send_create_signal('sitegate', ['EmailConfirmation'])


        # Changing field 'InvitationCode.acceptor'
        db.alter_column('sitegate_invitationcode', 'acceptor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['apps.User']))

        # Changing field 'InvitationCode.creator'
        db.alter_column('sitegate_invitationcode', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.User']))

    def backwards(self, orm):
        # Deleting model 'Preferences'
        db.delete_table('sitegate_preferences')

        # Deleting model 'EmailConfirmation'
        db.delete_table('sitegate_emailconfirmation')


        # Changing field 'InvitationCode.acceptor'
        db.alter_column('sitegate_invitationcode', 'acceptor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'InvitationCode.creator'
        db.alter_column('sitegate_invitationcode', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

    models = {
        'apps.place': {
            'Meta': {'object_name': 'Place'},
            'geo_bounds': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'blank': 'True'}),
            'geo_pos': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'blank': 'True'}),
            'geo_title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geo_type': ('django.db.models.fields.CharField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True', 'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raters_num': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'default': '0'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'auto_now': 'True', 'blank': 'True'}),
            'time_published': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user_title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'apps.user': {
            'Meta': {'object_name': 'User'},
            'comments_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'disqus_category_id': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30', 'blank': 'True'}),
            'disqus_shortname': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'users'", 'to': "orm['apps.Place']", 'blank': 'True'}),
            'raters_num': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'default': '0'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sitegate.blacklisteddomain': {
            'Meta': {'object_name': 'BlacklistedDomain'},
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '253'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sitegate.emailconfirmation': {
            'Meta': {'object_name': 'EmailConfirmation'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'expired': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_accepted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.User']"})
        },
        'sitegate.invitationcode': {
            'Meta': {'object_name': 'InvitationCode'},
            'acceptor': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'acceptors'", 'to': "orm['apps.User']", 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creators'", 'to': "orm['apps.User']"}),
            'expired': ('django.db.models.fields.BooleanField', [], {'db_index': 'True', 'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_accepted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'sitegate.preferences': {
            'Meta': {'object_name': 'Preferences'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signin_disabled_text': ('django.db.models.fields.TextField', [], {'default': "'Sign in is disabled.'"}),
            'signin_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signup_disabled_text': ('django.db.models.fields.TextField', [], {'default': "'Sign up is disabled.'"}),
            'signup_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signup_verify_email_body': ('django.db.models.fields.TextField', [], {'default': "'Please follow the link below to activate your account:\\n%(link)s'"}),
            'signup_verify_email_title': ('django.db.models.fields.CharField', [], {'max_length': '160', 'default': "'Account activation'"})
        }
    }

    complete_apps = ['sitegate']