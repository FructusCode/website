# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Payee.name'
        db.add_column('apwan_payee', 'name',
                      self.gf('django.db.models.fields.CharField')(default='My Payee', max_length=32),
                      keep_default=False)

        # Adding field 'Payee.slug'
        db.add_column('apwan_payee', 'slug',
                      self.gf('django.db.models.fields.CharField')(default='my-payee', max_length=32),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Payee.name'
        db.delete_column('apwan_payee', 'name')

        # Deleting field 'Payee.slug'
        db.delete_column('apwan_payee', 'slug')


    models = {
        'apwan.donation': {
            'Meta': {'object_name': 'Donation'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'USD'", 'max_length': '3'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payer_name': ('django.db.models.fields.CharField', [], {'default': "'Anonymous'", 'max_length': '64'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '12'}),
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
            'Meta': {'unique_together': "(('type', 'token'),)", 'object_name': 'Payee'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'apwan.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'payee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Payee']", 'null': 'True'}),
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