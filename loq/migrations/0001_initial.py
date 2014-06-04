# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Interval'
        db.create_table(u'loq_interval', (
            ('chr', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('start', self.gf('django.db.models.fields.IntegerField')(max_length=15)),
            ('stop', self.gf('django.db.models.fields.IntegerField')(max_length=15)),
            ('NeatName', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('IntervalSize', self.gf('django.db.models.fields.IntegerField')(max_length=45)),
            ('IntervalSerialNumber', self.gf('django.db.models.fields.SlugField')(max_length=45)),
            ('Structure', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('Annotations', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
            ('Tags', self.gf('django.db.models.fields.TextField')(max_length=100, blank=True)),
            ('Link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'loq', ['Interval'])

        # Adding unique constraint on 'Interval', fields ['chr', 'start', 'stop']
        db.create_unique(u'loq_interval', ['chr', 'start', 'stop'])

        # Adding model 'Library'
        db.create_table(u'loq_library', (
            ('library_id', self.gf('django.db.models.fields.CharField')(max_length=16, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('organism', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('strain', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('allele', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('tissue', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('target', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('resolution', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('source_org', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('source_person', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('five_prime_adapter_sequence', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('three_prime_adapter_sequence', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('multiplex_barcode_sequence', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=500, blank=True)),
        ))
        db.send_create_signal(u'loq', ['Library'])

        # Adding model 'Sequencing_Run'
        db.create_table(u'loq_sequencing_run', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seq_run_id', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('sequencing_center', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('release_status', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('GSM', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('GSE', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('modENCODE_id', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('mirror_track_group', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
        ))
        db.send_create_signal(u'loq', ['Sequencing_Run'])

        # Adding model 'Library_Sequencing_Run'
        db.create_table(u'loq_library_sequencing_run', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('library_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loq.Library'])),
            ('seq_run_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loq.Sequencing_Run'])),
        ))
        db.send_create_signal(u'loq', ['Library_Sequencing_Run'])

        # Adding model 'Genome_Build'
        db.create_table(u'loq_genome_build', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('genome_build_id', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal(u'loq', ['Genome_Build'])

        # Adding model 'Read_alignment'
        db.create_table(u'loq_read_alignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lib', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('sequence', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('read_counts', self.gf('django.db.models.fields.IntegerField')(max_length=45, null=True)),
            ('genomic_hits', self.gf('django.db.models.fields.IntegerField')(max_length=45)),
            ('chr', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('start', self.gf('django.db.models.fields.IntegerField')(max_length=45)),
            ('stop', self.gf('django.db.models.fields.IntegerField')(max_length=45)),
            ('strand', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('big2catrenormRPmirpre', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=15)),
            ('AGO1IPoverTotalRNA', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=15)),
            ('normReads', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=15)),
            ('structure', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal(u'loq', ['Read_alignment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Interval', fields ['chr', 'start', 'stop']
        db.delete_unique(u'loq_interval', ['chr', 'start', 'stop'])

        # Deleting model 'Interval'
        db.delete_table(u'loq_interval')

        # Deleting model 'Library'
        db.delete_table(u'loq_library')

        # Deleting model 'Sequencing_Run'
        db.delete_table(u'loq_sequencing_run')

        # Deleting model 'Library_Sequencing_Run'
        db.delete_table(u'loq_library_sequencing_run')

        # Deleting model 'Genome_Build'
        db.delete_table(u'loq_genome_build')

        # Deleting model 'Read_alignment'
        db.delete_table(u'loq_read_alignment')


    models = {
        u'loq.genome_build': {
            'Meta': {'object_name': 'Genome_Build'},
            'genome_build_id': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'loq.interval': {
            'Annotations': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'IntervalSerialNumber': ('django.db.models.fields.SlugField', [], {'max_length': '45'}),
            'IntervalSize': ('django.db.models.fields.IntegerField', [], {'max_length': '45'}),
            'Link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'Meta': {'unique_together': "(('chr', 'start', 'stop'),)", 'object_name': 'Interval'},
            'NeatName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'Structure': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Tags': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            'chr': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'start': ('django.db.models.fields.IntegerField', [], {'max_length': '15'}),
            'stop': ('django.db.models.fields.IntegerField', [], {'max_length': '15'})
        },
        u'loq.library': {
            'Meta': {'ordering': "['library_id']", 'object_name': 'Library'},
            'allele': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'five_prime_adapter_sequence': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'library_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'}),
            'multiplex_barcode_sequence': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'organism': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'source_org': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'source_person': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'strain': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'three_prime_adapter_sequence': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'tissue': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'})
        },
        u'loq.library_sequencing_run': {
            'Meta': {'object_name': 'Library_Sequencing_Run'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'library_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loq.Library']"}),
            'seq_run_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['loq.Sequencing_Run']"})
        },
        u'loq.read_alignment': {
            'AGO1IPoverTotalRNA': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '15'}),
            'Meta': {'object_name': 'Read_alignment'},
            'big2catrenormRPmirpre': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '15'}),
            'chr': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'genomic_hits': ('django.db.models.fields.IntegerField', [], {'max_length': '45'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lib': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'normReads': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '15'}),
            'read_counts': ('django.db.models.fields.IntegerField', [], {'max_length': '45', 'null': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'start': ('django.db.models.fields.IntegerField', [], {'max_length': '45'}),
            'stop': ('django.db.models.fields.IntegerField', [], {'max_length': '45'}),
            'strand': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'structure': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'})
        },
        u'loq.sequencing_run': {
            'GSE': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'GSM': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'Meta': {'object_name': 'Sequencing_Run'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mirror_track_group': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'modENCODE_id': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'release_status': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'seq_run_id': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'sequencing_center': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        }
    }

    complete_apps = ['loq']