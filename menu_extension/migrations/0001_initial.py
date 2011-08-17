# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MenuItemExtension'
        db.create_table('menu_extension_menuitemextension', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu_item', self.gf('django.db.models.fields.related.OneToOneField')(related_name='extension', unique=True, to=orm['treemenus.MenuItem'])),
            ('protected', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('menu_extension', ['MenuItemExtension'])


    def backwards(self, orm):
        
        # Deleting model 'MenuItemExtension'
        db.delete_table('menu_extension_menuitemextension')


    models = {
        'menu_extension.menuitemextension': {
            'Meta': {'object_name': 'MenuItemExtension'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_item': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'extension'", 'unique': 'True', 'to': "orm['treemenus.MenuItem']"}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'treemenus.menu': {
            'Meta': {'object_name': 'Menu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'root_item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'is_root_item_of'", 'null': 'True', 'to': "orm['treemenus.MenuItem']"})
        },
        'treemenus.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contained_items'", 'null': 'True', 'to': "orm['treemenus.Menu']"}),
            'named_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['treemenus.MenuItem']", 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['menu_extension']
