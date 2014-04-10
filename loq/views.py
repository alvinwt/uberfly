#from django.template import Template, Context
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import Http404,  HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from loq.models import Library_Sequencing_Run, Library, Interval, Read_alignment

import os
import matplotlib
import numpy as np
from numpy import array
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from loq.tables import IntervalTable, AlignTable
from django_tables2 import SingleTableView
from numpy.random import normal
import matplotlib.pyplot as plt
import StringIO

import pylab as p
import re
import random
import datetime
from itertools import chain 
from django_tables2 import RequestConfig
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio.Align.Applications import ClustalOmegaCommandline
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

class LibraryListView(ListView):
    model = Library
    context_object_name = 'library_id'

class AlignListAPIView(ListCreateAPIView):
    model = Read_alignment
    
class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        
class AlignSerializer(serializers.ModelSerializer):
    library_id = LibrarySerializer()
    
    class Meta: 
        model = Read_alignment
    
class AlignRetrieveAPIView(RetrieveUpdateAPIView):
    model = Read_alignment
    serializer_class = AlignSerializer
    
class AlignListView(ListView):
    model = Read_alignment
    template_name = 'srb/location.html'
    
    # def get_queryset(self):
    #     self.id = get_object_or_404(id)
    #     return Read_alignment.objects.filter(Read_alignment=self.id)
    
    def get_context_data(self, **kwargs):
        context = super(AlignListView,self).get_context_data(**kwargs)
        context['id'] = self.id
        return context

class IntView(ListView):
    template_name = 'srb/location.html'
    context_object_name = 'location_list'
    model = Interval

def align(request):
    table= AlignTable(Read_alignment.objects.all())
    RequestConfig(request).configure(table)
    return render(request,"srb/align.html",{'table':table})

def showStaticImage(request):
    #""" Simply return a static image as a png """
    imagePath = "plotResults.png"
    from PIL import Image
    Image.init()
    i = Image.open(imagePath)
    response = HttpResponse(mimetype='image/png')
    i.save(response,'PNG')
    return response


class AlignDetailView(DetailView):
    model = Read_alignment
    
    def get_sum(self):
        sum = self.object.read_counts +self.object.read_counts
        return sum

    def get_seq(self):
        stt = self.object.start 
        stp = self.object.stop +50

        for seq_record in SeqIO.parse('/home/alvin/Dropbox/FYP/Django/mysite/srb/media/dmel-3L-chromosome-r5.52.fasta','fasta'):
            seq = seq_record.seq
            # rev_seq = seq_record.seq.reverse_complement()
            if self.object.strand == '+':
                s = str(seq[stt:stp])
            else:
                s =  str(seq[stt:stp].reverse_complement())
            return s
            
    def get_mapping(self):
        #get sequences that are in the region, currently hard coded, can be done with intervals specified.
        dob= self.object
        if int(dob.start) - 20 <= 0:
           start = int(dob.start)
        else:
            start = int(dob.start-50)
        stop = dob.stop + 20 
        seq = Read_alignment.objects.filter(chr=dob.chr,strand=dob.strand, start__gte=start,stop__lte=stop).values_list('id','sequence')
        seqArray= array(seq)
        s = []
        for i in seqArray:
            s.append(">"+ i[0] + "\n"+ i[1] +"\n")
        clustalo_cline= ClustalOmegaCommandline(infile='-')
        stdout,stderr=clustalo_cline("".join(s))
        stdout = re.sub(r'(?<=\d)\n',' ',stdout)
        return stdout
        
    
    def get_context_data(self, **kwargs):
        context = super(AlignDetailView,self).get_context_data(**kwargs)
        #      context['graph'] = self.graph()
        context['sum'] = self.get_sum()
        context['seq'] = self.get_seq()
        context['msa'] = self.get_mapping()
        return context
    
    # def align(request):
    #     table= AlignTable()
    #     RequestConfig(request).configure(table)
    #     return render(request,"srb/read_alignment_detail.html",{'table':table,}
                      

# class AlignDetail(SingleTableView):
#     model = Read_alignment
#     table_class = AlignTable
    # coordinate using table2
    
def coordinate(request):
    all = Interval.objects.all()
    coordinates= CoordinateTable(all)
    avg_counts = CoordinateTable(Read_alignment.objects.annotate(Avg('read_counts'))) 
    config = RequestConfig(request)
    config.configure(coordinates)
    config.configure(avg_counts)
    return render(request,"srb/coordinate.html",{'coordinates':coordinates,'avg_counts':avg_counts })


    
