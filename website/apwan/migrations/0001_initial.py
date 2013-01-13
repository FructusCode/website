# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Payee'
        db.create_table('apwan_payee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('account_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('apwan', ['Payee'])

        # Adding model 'Recipient'
        db.create_table('apwan_recipient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('payee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apwan.Payee'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('apwan', ['Recipient'])

        # Adding model 'Entity'
        db.create_table('apwan_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apwan.Recipient'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('apwan', ['Entity'])

        # Adding model 'Donation'
        db.create_table('apwan_donation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apwan.Entity'])),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('payer_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('tip', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('account_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('apwan', ['Donation'])


    def backwards(self, orm):
        # Deleting model 'Payee'
        db.delete_table('apwan_payee')

        # Deleting model 'Recipient'
        db.delete_table('apwan_recipient')

        # Deleting model 'Entity'
        db.delete_table('apwan_entity')

        # Deleting model 'Donation'
        db.delete_table('apwan_donation')


    models = {
        'apwan.donation': {
            'Meta': {'object_name': 'Donation'},
            'account_id': ('django.db.models.fields.IntegerField', [], {}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payer_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'tip': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'apwan.entity': {
            'Meta': {'object_name': 'Entity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Recipient']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'apwan.payee': {
            'Meta': {'object_name': 'Payee'},
            'account_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'apwan.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'payee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apwan.Payee']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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