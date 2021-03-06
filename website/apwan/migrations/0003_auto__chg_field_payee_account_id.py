# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Payee.account_id'
        db.alter_column('apwan_payee', 'account_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    def backwards(self, orm):

        # Changing field 'Payee.account_id'
        db.alter_column('apwan_payee', 'account_id', self.gf('django.db.models.fields.IntegerField')(null=True))

    models = {
        'apwan.donation': {
            'Meta': {'object_name': 'Donation'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'checkout_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Payee']", 'null': 'True'}),
            'payer_name': ('django.db.models.fields.CharField', [], {'default': "'Anonymous'", 'max_length': '64'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Recipient']", 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '12'}),
            'tip': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'})
        },
        'apwan.entity': {
            'Meta': {'object_name': 'Entity'},
            'album': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Entity']", 'null': 'True'}),
            'recipient': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['apwan.Recipient']", 'symmetrical': 'False'}),
            's_album': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            's_artist': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            's_title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            's_track': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'suggested_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'track': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True'})
        },
        'apwan.entityreference': {
            'Meta': {'object_name': 'EntityReference'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'apwan.payee': {
            'Meta': {'object_name': 'Payee'},
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'account_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'userservice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Service']", 'null': 'True'})
        },
        'apwan.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'payee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Payee']", 'null': 'True', 'blank': 'True'}),
            's_title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'apwan.recipientreference': {
            'Meta': {'object_name': 'RecipientReference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Recipient']"}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'apwan.service': {
            'Meta': {'unique_together': "(('service', 'service_id'),)", 'object_name': 'Service'},
            'data': ('json_field.fields.JSONField', [], {'default': "'null'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'service_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'service_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'apwan.token': {
            'Meta': {'object_name': 'Token'},
            'data': ('json_field.fields.JSONField', [], {'default': "'null'", 'null': 'True', 'blank': 'True'}),
            'expire': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'token_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'apwan.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'deployauth_token': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preferred_contact_method': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['apwan']