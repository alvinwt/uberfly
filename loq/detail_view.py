from django.views.generic import DetailView
from loq.models import Read_alignment, Interval
from reportlab.pdfgen import canvas
from django.http import HttpResponse
#from GChartWrapper import *

import re
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio.Align.Applications import ClustalOmegaCommandline

import numpy as np
from numpy import array
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure
#from graph import plotResults

from django.shortcuts import render
from django_tables2 import RequestConfig, SingleTableMixin
from tables import DetailTable
import pysam



class AlignDetailView(SingleTableMixin,DetailView):
    model= Read_alignment
    table_class = DetailTable
    context_table_name = 'detail'

    def get_table_data (self):
        table_data= Read_alignment.objects.filter(intervalName=self.object.intervalName)
        return table_data

    # def get_sum(self):
    #     sum = self.object.read_counts +self.object.read_counts
    #     return sum

    def get_seq(self):
        if Interval.objects.filter(NeatName=self.object.intervalName).exists():
            stt = self.object.start 
            stp = self.object.stop +20
        else:
            stt = self.object.intervalName.start
            stp = self.object.intervalName.stop
            
            chrom = str(self.object.chr).replace('chr','')
            fasta_file= '/home/lichenhao/Dropbox/djangosite/loq/static/fasta/dmel-' + chrom+ '-chromosome-r5.50.fasta'
        #still hardcoded! needs to be static*
        for seq_record in SeqIO.parse(fasta_file,'fasta'):
            seq = seq_record.seq
            # rev_seq = seq_record.seq.reverse_complement()
            if self.object.strand == '+':
                seqInterval = str(seq[stt:stp])
            else:
                seqInterval =  str(seq[stt:stp].reverse_complement())
            return seqInterval
            
    def get_mapping(self):
        #get sequences that are in the region, currently hard coded, can be done with intervals specified.
        dob= self.object
        if int(dob.start) - 20 <= 0:
           start = int(dob.start)
        else:
            start = int(dob.start)
        stop = dob.stop + 20 
        seq = Read_alignment.objects.filter(chr=dob.chr,strand=dob.strand, start__gte=start,stop__lte=stop).values_list('id','sequence')
        seqArray= array(seq)
        s = []
        for i in seqArray:
            s.append(">"+ i[0] + "\n"+ i[1] +"\n")
        clustalo_cline= ClustalOmegaCommandline(infile='-')
        stdout,stderr=clustalo_cline("".join(s))
        stdout = re.sub(r'(?<=\d)\n(\w)','',stdout)
        stdout = re.sub(r'>\d+','',stdout)
        return stdout

    def get_alignment(self):
        self = self.object
        if self.intervalName == False:
            stt = self.start 
            stp = self.stop +20
        else:
            stt = self.intervalName.start
            stp = self.intervalName.stop
            
        alignment = Read_alignment.objects.filter(chr= self.chr, start__gte= stt , stop__lte=stp,strand=self.strand)
        string =""
        for i in alignment:
            pretty = '%s \t\t %s\n' % (i.sequence, str(i.read_counts))
            cord = int(i.start)-stt
            if cord >= 1:
               string += cord * ' ' + pretty 
            else:
               string += pretty
        return string
                
    # gets pileup from BAM file to give readcounts per Nt. data is then return as a list in numpy array for plotting in google charts
    # nb: chr reference can be '2L' or coded depending on BAM file. consider splitting string into chr | 2L before coding
    #needs testing 
    def get_graph(self):
        bamFile= pysam.Samfile('/home/alvin/Dropbox/SmallRNABiogenesis/testdata/V063V0632.sorted.bam', 'rb')
        bam = []
        self =self.object
        if self.intervalName == False:
            stt = self.start 
            stp = self.stop +20
        else:
            stt = self.intervalName.start
            stp = self.intervalName.stop
        for pile in bamFile.pileup('chr3L',stt,stp):
            bam.append([pile.pos,pile.n])
        bamFile.close
        return bam

    def get_read_counts(self):
        dob= self.object
        if int(dob.start) - 20 <= 0:
           start = int(dob.start)
        else:
            start = int(dob.start-20)
        stop = dob.stop + 20 
        count = Read_alignment.objects.filter(chr=dob.chr,strand=dob.strand, start__gte=start,stop__lte=stop).values_list('start','stop','read_counts')
        return count

    def align_view(request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment;filename=test.pdf'
        p= canvas.Canvas(response)
        p.drawString(100,100,"hello world")
        p.showPage()
        p.save()
        return response
     
    def get_context_data(self, **kwargs):
        context = super(AlignDetailView,self).get_context_data(**kwargs)
        #context['sum'] = self.get_sum()
        context['seq'] = self.get_seq()
        context['msa'] = self.get_alignment()
        context['cts'] = self.get_read_counts()
        #context['graph'] = self.get_graph()
        return context

