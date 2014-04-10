import matplotlib as mpl
mpl.use('Agg')
from django.core.urlresolvers import reverse
from django.shortcuts import render
import pandas as pd
import numpy as np
from django.db.models import Count, Sum
import matplotlib.pyplot as plt
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from loq.models import Interval ,Read_alignment, Library
from loq.forms import GraphForm
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Count, Sum
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import cStringIO
from reportlab.lib.units import inch, cm
sns.set(style='whitegrid',palette="hls",context='talk')
# sns.set(style='whitegrid',palette=["#000000", "#E69F00", "#56B4E9", "#009E73", "#8C1515", "#D55E00", "#CC79A7"],context='talk')


def plot_graph(name,libraries,chart_type,normal,style):
    """Retrieves the values from the database with the entries mapped in the form and returns a graph"""
    interval_object = Interval.objects.select_related().get(mirName__icontains=name)
    read_object= interval_object.read_alignment_set.filter(lib__in=libraries).order_by('lib')
    len_count =read_object.values('read_length','lib','read_counts','intervalName__sum_read_counts','normReads').annotate(Count('read_length')).order_by('read_length')
    lib_total_count =read_object.values('lib').annotate(Sum('read_counts'))

    #Generates a list of read lengths
    length=[]
    for i in len_count:
        length.append(int(i['read_length']))
    lengths_reads = sorted(set(length))

        #Generate dataframe, fills it with 0s and intiate a dict with lib:read count values 
    df = pd.DataFrame(index=lengths_reads, columns=libraries, dtype='float64')
    df = df.fillna(0).convert_objects()
    d= {}                
    for j in lib_total_count:
        d[j['lib']] = j['read_counts__sum']

        # Fills the dataframe with values accessing using library id and read_length
        # This allows for choosing which way of normalizing    
    for i in len_count:
        lb=i['lib']
        lh=i['read_length']
       
        if normal == 'dist_rpm':
            data = i['read_length__count']*i['normReads']
            title = 'Reads per million'
           
        elif normal == 'dist_read_counts':
            data = i['read_length__count']*i['read_counts']
            title = 'Reads Counts'
        else: 
            data = (100*float(i['read_length__count']*i['read_counts']))/float(d[i['lib']])
            title ='Read counts per miRNA mapped'
            
        df[lb][lh] += data
    
     # Draws the figure 
    fig= plt.figure(figsize=(8.27, 11.69), dpi=200)
    ax = fig.add_subplot(111)
    graph = df.plot(ax=ax ,style=style,kind=chart_type,figsize=(10,8),subplots=False,legend=False)
    handles, labels = graph.get_legend_handles_labels()
    #graph.legend(handles, labels)
    graph.legend(handles,[i+' '+str(df[i].sum().round(2)) for i in libraries], title= 'Library : Total ')
    plt.title('Read Length Distribution of '+ str(interval_object.mirName))
    plt.xlabel('Length of Read')
    plt.grid(True)
    plt.ylabel(title)
    plt.tight_layout()
    
    # Adds in the coordinates      
    cord_df = df.stack(0).reset_index(0)
    cord_df['z']= cord_df[0]
    cord_arr = np.array(cord_df)
    cord_tup = (map(tuple,cord_arr))
    
    for i in cord_tup:
        if i[1] == 0:
            pass
        else:
            if i[2] % 1 == 0:
               num = int(i[2])
            else:
                num = "%.2f"%i[2]
            plt.annotate(num , (int(i[0]),int(i[1])), xytext=(int(i[0]),int(i[1])), fontsize=12)
    
    
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] ='attachment; filename =' + str(interval_object.mirName)+ '.pdf'
    imagedata=cStringIO.StringIO()
    fig.savefig(imagedata, format='png')
    imagedata.seek(0)
    image = ImageReader(imagedata)
    p= canvas.Canvas(response)
    p.drawImage(image,0,0,8.27 * cm,11.69 * cm,preserveAspectRatio=True)
    p.showPage()
    p.save()
    return response



def Graph_Form(request):
    errors = []
    if request.user.is_authenticated():
        if request.method == 'POST':
            if not request.POST.get('mirName',''):
                errors.append("Enter a miRNA name")
            form = GraphForm(request.POST)
            if form.is_valid():
                name= form.cleaned_data['mirName']
                libraries = form.cleaned_data['Library']
                chart_type = form.cleaned_data['Chart']
                if chart_type == 'line':
                    style = 'o-'
                else :
                    style = None
                normal = form.cleaned_data['Normal']
                try:
                    response =  plot_graph(name,libraries,chart_type,normal,style)
                    return response 
                    # return HttpResponseRedirect(reverse('IntervalDetailView', kwargs={'pk': interval_object.pk}))
                except (MultipleObjectsReturned), e :
                    return HttpResponse("Please provide a specific query. Your search returned more than one result.")
            
                except ObjectDoesNotExist:
                    return HttpResponse("Please check your query, the miRNA does not exist in the database.")
            else:
                form = GraphForm()
                errors.append('Please choose all the fields before selecting')
                return render(request,'loq/graph_filter.html',{'form':form,'errors':errors })
                
        else:
            form = GraphForm()
            #errors.append('Please choose all the fields before selecting')
            return render(request,'loq/graph_filter.html',{'form':form,'errors':errors })
    else:
        return HttpResponseRedirect('/login/')
