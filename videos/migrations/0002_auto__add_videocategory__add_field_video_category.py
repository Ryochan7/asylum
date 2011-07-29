# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'VideoCategory'
        db.create_table('videos_videocategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('videos', ['VideoCategory'])
        orm["videos.VideoCategory"].objects.create (title="Uncategorized", slug="uncategorized")

        # Adding field 'Video.category'
        db.add_column('videos_video', 'category', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['videos.VideoCategory']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'VideoCategory'
        db.delete_table('videos_videocategory')

        # Deleting field 'Video.category'
        db.delete_column('videos_video', 'category_id')


    models = {
        'videos.video': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Video'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['videos.VideoCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '512', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'video_url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'videos.videocategory': {
            'Meta': {'object_name': 'VideoCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['videos']
