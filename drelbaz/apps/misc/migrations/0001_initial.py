# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DentalClinic'
        db.create_table(u'misc_dentalclinic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('dentist', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
        ))
        db.send_create_signal(u'misc', ['DentalClinic'])

        # Adding model 'Blog'
        db.create_table(u'misc_blog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=10000)),
        ))
        db.send_create_signal(u'misc', ['Blog'])


    def backwards(self, orm):
        # Deleting model 'DentalClinic'
        db.delete_table(u'misc_dentalclinic')

        # Deleting model 'Blog'
        db.delete_table(u'misc_blog')


    models = {
        u'misc.blog': {
            'Meta': {'object_name': 'Blog'},
            'content': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'misc.dentalclinic': {
            'Meta': {'object_name': 'DentalClinic'},
            'dentist': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        }
    }

    complete_apps = ['misc']