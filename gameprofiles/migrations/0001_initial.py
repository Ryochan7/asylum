# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Platform'
        db.create_table(u'gameprofiles_platform', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2000, null=True, blank=True)),
            ('icon', self.gf('mezzanine.core.fields.FileField')(max_length=255)),
        ))
        db.send_create_signal(u'gameprofiles', ['Platform'])

        # Adding model 'Application'
        db.create_table(u'gameprofiles_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2000, null=True, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('boxart', self.gf('mezzanine.core.fields.FileField')(max_length=255)),
        ))
        db.send_create_signal(u'gameprofiles', ['Application'])

        # Adding M2M table for field platforms on 'Application'
        m2m_table_name = db.shorten_name(u'gameprofiles_application_platforms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('application', models.ForeignKey(orm[u'gameprofiles.application'], null=False)),
            ('platform', models.ForeignKey(orm[u'gameprofiles.platform'], null=False))
        ))
        db.create_unique(m2m_table_name, ['application_id', 'platform_id'])

        # Adding model 'Screenshot'
        db.create_table(u'gameprofiles_screenshot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameprofiles.Application'])),
            ('image', self.gf('mezzanine.core.fields.FileField')(max_length=255)),
        ))
        db.send_create_signal(u'gameprofiles', ['Screenshot'])

        # Adding model 'Controller'
        db.create_table(u'gameprofiles_controller', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
        ))
        db.send_create_signal(u'gameprofiles', ['Controller'])

        # Adding M2M table for field platforms on 'Controller'
        m2m_table_name = db.shorten_name(u'gameprofiles_controller_platforms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('controller', models.ForeignKey(orm[u'gameprofiles.controller'], null=False)),
            ('platform', models.ForeignKey(orm[u'gameprofiles.platform'], null=False))
        ))
        db.create_unique(m2m_table_name, ['controller_id', 'platform_id'])

        # Adding model 'Profile'
        db.create_table(u'gameprofiles_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('file', self.gf('mezzanine.core.fields.FileField')(max_length=255)),
            ('download_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('controller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameprofiles.Controller'])),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameprofiles.Application'])),
        ))
        db.send_create_signal(u'gameprofiles', ['Profile'])

        # Adding model 'FeaturedProfile'
        db.create_table(u'gameprofiles_featuredprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gameprofiles.Application'], unique=True)),
            ('profile', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gameprofiles.Profile'], unique=True)),
        ))
        db.send_create_signal(u'gameprofiles', ['FeaturedProfile'])

        # Adding unique constraint on 'FeaturedProfile', fields ['application', 'profile']
        db.create_unique(u'gameprofiles_featuredprofile', ['application_id', 'profile_id'])

        # Adding model 'ProfileDownload'
        db.create_table(u'gameprofiles_profiledownload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ipaddress', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gameprofiles.Profile'])),
            ('accessed', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'gameprofiles', ['ProfileDownload'])

        # Adding unique constraint on 'ProfileDownload', fields ['ipaddress', 'profile']
        db.create_unique(u'gameprofiles_profiledownload', ['ipaddress', 'profile_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProfileDownload', fields ['ipaddress', 'profile']
        db.delete_unique(u'gameprofiles_profiledownload', ['ipaddress', 'profile_id'])

        # Removing unique constraint on 'FeaturedProfile', fields ['application', 'profile']
        db.delete_unique(u'gameprofiles_featuredprofile', ['application_id', 'profile_id'])

        # Deleting model 'Platform'
        db.delete_table(u'gameprofiles_platform')

        # Deleting model 'Application'
        db.delete_table(u'gameprofiles_application')

        # Removing M2M table for field platforms on 'Application'
        db.delete_table(db.shorten_name(u'gameprofiles_application_platforms'))

        # Deleting model 'Screenshot'
        db.delete_table(u'gameprofiles_screenshot')

        # Deleting model 'Controller'
        db.delete_table(u'gameprofiles_controller')

        # Removing M2M table for field platforms on 'Controller'
        db.delete_table(db.shorten_name(u'gameprofiles_controller_platforms'))

        # Deleting model 'Profile'
        db.delete_table(u'gameprofiles_profile')

        # Deleting model 'FeaturedProfile'
        db.delete_table(u'gameprofiles_featuredprofile')

        # Deleting model 'ProfileDownload'
        db.delete_table(u'gameprofiles_profiledownload')


    models = {
        u'gameprofiles.application': {
            'Meta': {'object_name': 'Application'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'boxart': ('mezzanine.core.fields.FileField', [], {'max_length': '255'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'platforms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gameprofiles.Platform']", 'symmetrical': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'gameprofiles.controller': {
            'Meta': {'object_name': 'Controller'},
            'guid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'platforms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gameprofiles.Platform']", 'symmetrical': 'False'})
        },
        u'gameprofiles.featuredprofile': {
            'Meta': {'unique_together': "(('application', 'profile'),)", 'object_name': 'FeaturedProfile'},
            'application': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['gameprofiles.Application']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['gameprofiles.Profile']", 'unique': 'True'})
        },
        u'gameprofiles.platform': {
            'Meta': {'object_name': 'Platform'},
            'icon': ('mezzanine.core.fields.FileField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'gameprofiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameprofiles.Application']"}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'controller': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameprofiles.Controller']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'file': ('mezzanine.core.fields.FileField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'gameprofiles.profiledownload': {
            'Meta': {'unique_together': "(('ipaddress', 'profile'),)", 'object_name': 'ProfileDownload'},
            'accessed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddress': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameprofiles.Profile']"})
        },
        u'gameprofiles.screenshot': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Screenshot'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gameprofiles.Application']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('mezzanine.core.fields.FileField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['gameprofiles']