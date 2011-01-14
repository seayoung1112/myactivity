# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Friendship'
        db.create_table('friends_friendship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friends', to=orm['auth.User'])),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_unused_', to=orm['auth.User'])),
            ('added', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
        ))
        db.send_create_signal('friends', ['Friendship'])

        # Adding unique constraint on 'Friendship', fields ['to_user', 'from_user']
        db.create_unique('friends_friendship', ['to_user_id', 'from_user_id'])

        # Adding model 'FriendApplication'
        db.create_table('friends_friendapplication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friends_applying', to=orm['auth.User'])),
            ('apply_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friends_applied', to=orm['auth.User'])),
        ))
        db.send_create_signal('friends', ['FriendApplication'])

        # Adding unique constraint on 'FriendApplication', fields ['applicant', 'apply_object']
        db.create_unique('friends_friendapplication', ['applicant_id', 'apply_object_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FriendApplication', fields ['applicant', 'apply_object']
        db.delete_unique('friends_friendapplication', ['applicant_id', 'apply_object_id'])

        # Removing unique constraint on 'Friendship', fields ['to_user', 'from_user']
        db.delete_unique('friends_friendship', ['to_user_id', 'from_user_id'])

        # Deleting model 'Friendship'
        db.delete_table('friends_friendship')

        # Deleting model 'FriendApplication'
        db.delete_table('friends_friendapplication')


    models = {
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
        },
        'friends.friendapplication': {
            'Meta': {'unique_together': "(('applicant', 'apply_object'),)", 'object_name': 'FriendApplication'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friends_applying'", 'to': "orm['auth.User']"}),
            'apply_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friends_applied'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'friends.friendship': {
            'Meta': {'unique_together': "[('to_user', 'from_user')]", 'object_name': 'Friendship'},
            'added': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_unused_'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friends'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['friends']
