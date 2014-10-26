# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DeviceToken'
        db.create_table(u'accounts_devicetoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['DeviceToken'])

        # Adding model 'Photo'
        db.create_table(u'accounts_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('image_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('thumbnail_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('thumbnail_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dentist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['Photo'])

        # Adding model 'Book'
        db.create_table(u'accounts_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('dentist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['Book'])

        # Adding model 'UserProfile'
        db.create_table(u'accounts_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contact_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('dentist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='patient', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'accounts', ['UserProfile'])

        # Adding M2M table for field device_token on 'UserProfile'
        m2m_table_name = db.shorten_name(u'accounts_userprofile_device_token')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('devicetoken', models.ForeignKey(orm[u'accounts.devicetoken'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'devicetoken_id'])

        # Adding model 'DentistProfile'
        db.create_table(u'accounts_dentistprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('map', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('patient_education', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dentist', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['DentistProfile'])

        # Adding M2M table for field device_token on 'DentistProfile'
        m2m_table_name = db.shorten_name(u'accounts_dentistprofile_device_token')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dentistprofile', models.ForeignKey(orm[u'accounts.dentistprofile'], null=False)),
            ('devicetoken', models.ForeignKey(orm[u'accounts.devicetoken'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dentistprofile_id', 'devicetoken_id'])

        # Adding model 'Notification'
        db.create_table(u'accounts_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'accounts', ['Notification'])

        # Adding model 'Note'
        db.create_table(u'accounts_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'accounts', ['Note'])

        # Adding model 'EmergencySchedule'
        db.create_table(u'accounts_emergencyschedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dentist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('is_booked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['EmergencySchedule'])

        # Adding unique constraint on 'EmergencySchedule', fields ['dentist', 'date', 'time']
        db.create_unique(u'accounts_emergencyschedule', ['dentist_id', 'date', 'time'])

        # Adding model 'Appointment'
        db.create_table(u'accounts_appointment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('dentist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dentist_apts', to=orm['auth.User'])),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='patient_apts', to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=10)),
        ))
        db.send_create_signal(u'accounts', ['Appointment'])


    def backwards(self, orm):
        # Removing unique constraint on 'EmergencySchedule', fields ['dentist', 'date', 'time']
        db.delete_unique(u'accounts_emergencyschedule', ['dentist_id', 'date', 'time'])

        # Deleting model 'DeviceToken'
        db.delete_table(u'accounts_devicetoken')

        # Deleting model 'Photo'
        db.delete_table(u'accounts_photo')

        # Deleting model 'Book'
        db.delete_table(u'accounts_book')

        # Deleting model 'UserProfile'
        db.delete_table(u'accounts_userprofile')

        # Removing M2M table for field device_token on 'UserProfile'
        db.delete_table(db.shorten_name(u'accounts_userprofile_device_token'))

        # Deleting model 'DentistProfile'
        db.delete_table(u'accounts_dentistprofile')

        # Removing M2M table for field device_token on 'DentistProfile'
        db.delete_table(db.shorten_name(u'accounts_dentistprofile_device_token'))

        # Deleting model 'Notification'
        db.delete_table(u'accounts_notification')

        # Deleting model 'Note'
        db.delete_table(u'accounts_note')

        # Deleting model 'EmergencySchedule'
        db.delete_table(u'accounts_emergencyschedule')

        # Deleting model 'Appointment'
        db.delete_table(u'accounts_appointment')


    models = {
        u'accounts.appointment': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Appointment'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'dentist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dentist_apts'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'patient_apts'", 'to': u"orm['auth.User']"}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '10'}),
            'time': ('django.db.models.fields.TimeField', [], {})
        },
        u'accounts.book': {
            'Meta': {'object_name': 'Book'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dentist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'accounts.dentistprofile': {
            'Meta': {'object_name': 'DentistProfile'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'dentist': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'device_token': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['accounts.DeviceToken']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'patient_education': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'accounts.devicetoken': {
            'Meta': {'object_name': 'DeviceToken'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        u'accounts.emergencyschedule': {
            'Meta': {'ordering': "('-date', 'time')", 'unique_together': "(('dentist', 'date', 'time'),)", 'object_name': 'EmergencySchedule'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'dentist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_booked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time': ('django.db.models.fields.TimeField', [], {})
        },
        u'accounts.note': {
            'Meta': {'object_name': 'Note'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'accounts.notification': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Notification'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'accounts.photo': {
            'Meta': {'object_name': 'Photo'},
            'dentist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'thumbnail_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'dentist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'patient'", 'to': u"orm['auth.User']"}),
            'device_token': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['accounts.DeviceToken']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']