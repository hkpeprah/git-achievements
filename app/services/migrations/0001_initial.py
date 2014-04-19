# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'services_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('service', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('payload', self.gf('jsonfield.fields.JSONField')(default={})),
            ('attributes', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'services', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'services_event')


    models = {
        u'services.event': {
            'Meta': {'object_name': 'Event'},
            'attributes': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'payload': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '90'})
        }
    }

    complete_apps = ['services']