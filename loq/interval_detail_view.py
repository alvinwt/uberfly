from django.views.generic import DetailView
from .models import Read_alignment, Interval, Library
from graph_view import plot_graph
import os
from django_tables2 import RequestConfig, SingleTableMixin
import re
from Bio import SeqIO
import numpy as np
import pandas as pd
from django.contrib.auth.decorators import login_required
from tables import DetailTable
from django.utils.decorators import method_decorator
from django.db.models import Count


"""This file generates the elements in each detail page of the miRNA entries."""
class IntervalDetailView(SingleTableMixin,DetailView):
    model= Interval
    table_class = DetailTable
    context_table_name = 'interval_detail'


    ### Requires login and authorization that is provided in the admin interface
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IntervalDetailView,self).dispatch(*args, **kwargs)

    ### Returns basic data of the read alignments mapped to this interval
    def get_table_data (self):
        table_data= Read_alignment.objects.filter(intervalName=self.object)
        return table_data

    ### Uses the Chromosome, genomic start and stop positions to parse the sequence from a FASTA file
    def get_seq(self):
        stt = self.object.start 
        stp = self.object.stop
        
        ### This is where to change the filenames of the FASTA files esp when the genome build changes
        chrom = str(self.object.chr).replace('chr','')
        fasta_file= os.getcwd() + '/static/fasta/dmel-' + chrom+ '-chromosome-r5.54.fasta'

        for seq_record in SeqIO.parse(fasta_file,'fasta'):
            seq = seq_record.seq
            seqInterval = seq[stt:stp]
            if self.object.mapped_strand == "+":
                seqInterval = str(seq[stt:stp])
            else:
                seqInterval = str(seq[stt:stp].reverse_complement())
        return seqInterval
    
    ### Generates the sequence alignment according to the difference of the start and stop postions, adding a space for each nt that is different.
    ### This only works if the reads are not outside of the defined interval, reads spanning the interval will be forced to fit at the ends.
    
    def get_msa(self):
        self = self.object

        ### retrieves reads that map to the interval, cound seq returns a count of all reads which have the same read sequence.
        read_list=Read_alignment.objects.filter(intervalName=self, strand=self.mapped_strand).order_by('lib').select_related().order_by('start')
        count_seq=  read_list.values('sequence','start','stop','rev_sequence').annotate(Count('sequence'))
        all_libs = read_list.values('library__rescue').annotate(Count('library__rescue'))
        allseqs =[]
        string ="\n\n"
        libs = []
        
        for i in count_seq:
            if len(i['sequence']) == i['stop']-i['start']:
                allseqs.append(i['sequence'])
            else:
                pass

        #### all_libs return a list of libraries that the reads are from 
        for i in all_libs:
            libs.append(i['library__rescue'])
            #libs = sorted(libs)
        df = pd.DataFrame(index=allseqs,columns =libs,dtype='float64')

        ### Enters the counts of each sequence and the library they are from into a dataframe
        for i in read_list:
            if len(i.sequence) == int(i.stop)-int(i.start):
                df[i.library.rescue][i.sequence] ='%.2f' % i.normReads
            else:
                pass

   
        counts = df.to_string(index=None, na_rep ='-',sparsify=True)
        
        ### Generates the MSA by deducting difference between end of interval and start of sequence
        ### The script does it differently for + and - strand intervals. 
        for j in count_seq:
            if len(j['sequence']) == j['stop']-j['start']:
                spaces = int(j['start'])-int(self.start)  
                if self.mapped_strand == '+':
                    reads = '%s\n' % j['sequence']
                    if spaces >= 1:
                        string += spaces * ' ' + reads 
                    else:
                        string += reads
           
                else:
                    reads = '%s\n' % j['sequence']
                    spaces = int(self.stop)-int(j['stop']) 
                    if spaces >= 1:
                        string += spaces * ' ' + reads
                    else:
                        string += reads
            else:
                pass
            
        return {'string':string, 'counts': counts}

    ### Generates the pileup using a dataframe with coordinates as keys.
    ### The output data is then formatted to give a string which can be read by the googlecharts API
    
    def get_graph2(self):
        self=self.object
        reads= Read_alignment.objects.filter(intervalName=self,strand=self.mapped_strand).order_by('lib')
        ### Gets a list of libs 
        libs = []
        for lib_object in Library.objects.all().order_by('library_id'):
            libs.append(str(lib_object.rescue))
            
        ### Generates a list of range from the start to end of the interval    
        cords = np.arange(self.start-1,self.stop+1,dtype='int64')
        
        ### Draws the dataframe
        df = pd.DataFrame(index=cords, columns=libs, dtype='float64')

        ### Fills it with 0s for me to add read counts to
        df = df.fillna(0).convert_objects()

        ### Hideous 'for' loop that breaks the reads into individual nts and adds the readcounts to the dataframe after accessing using the library and j(nt position)
        for i in reads:
            for j in range(i.start,i.stop):
                df[i.library.rescue][j] += i.normReads

        ### Generates a column of empty values and calling the mid_point value in the db and plotting it        
        df['Mid Point'] = pd.Series(np.zeros(len(cords)), index=df.index)
        max_value =df.max().max() 
        df['Mid Point'][self.mid_point] += max_value 

        ### Reshapes the data and formats as a string. To debug, just throw the entire output as a template tag {{graph}} and you will see the ugly string 
        a= np.array(np.round(df,4))
        w = np.reshape(cords,(len(cords),-1))       
        list = np.concatenate((w,a),axis=1)
        if self.mapped_strand == "-":
            list = np.flipud(list)
        else: 
            pass
        list = list.tolist()
        for i in list:
            i[0] = int(i[0])
        libs.insert(0,"Coordinates")
        libs.insert(len(libs),'Mid point')
        list.insert(0,libs)

        for i in list:
            i[0] = str(i[0])
    
        return list
    # def get_dist(self):
    #    self = self.object
    #    name = self.mirName
    #    lib= Library.objects.all().values_list('rescue',flat=True)
    #    chart = 'bar'
    #    norm = 'dist_read_counts'
    #    plot = plot_graph(name,lib,chart,norm,None)
    #    return plot
    
    ### Provides the output from previous functions into the Django page 
    def get_context_data(self, **kwargs):
        context = super(IntervalDetailView,self).get_context_data(**kwargs)
        context['seq'] = self.get_seq()
        context['msa'] = self.get_msa()['string']
        context['graph']= self.get_graph2()
        context['counts']=self.get_msa()['counts']
        #context['dist']=self.get_dist() 
        # context['lib'] = self.get_libname()
        return context
    
