# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Privacy'
        db.create_table('privacy_privacy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('allow_stranger_invite', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('privacy', ['Privacy'])


    def backwards(self, orm):
        
        # Deleting model 'Privacy'
        db.delete_table('privacy_privacy')


    models = {
        'privacy.privacy': {
            'Meta': {'object_name': 'Privacy'},
            'allow_stranger_invite': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['privacy']
