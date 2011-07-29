# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm["videos.VideoCategory"].objects.create (title="Uncategorized", slug="uncategorized")


    def backwards(self, orm):
        "Write your backwards methods here."
        orm["videos.VideoCategory"].objects.delete ()


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
