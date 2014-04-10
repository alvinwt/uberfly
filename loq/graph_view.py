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
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
#sns.set(style='whitegrid',palette="hls",context='poster')
#sns.set(style='whitegrid',palette=["#000000", "#E69F00", "#56B4E9", "#009E73", "#8C1515", "#D55E00", "#CC79A7"],context='poster')
sns.set(palette=['#088A08','#0000FF','#FF0000','#58FA58','#2E9AFE','#FFBF00'],context='poster',style='whitegrid')
pgf_with_custom_preamble = { 'text.usetex':True,
                            'text.latex.unicode':True,
                            'text.latex.preamble':[r"\usepackage{booktabs}"]
                            }
mpl.rcParams.update(pgf_with_custom_preamble)


def plot_graph(name,libraries,chart_type,normal,style):
    """Retrieves the values from the database with the entries mapped in the form and returns a graph"""    
    interval_object = Interval.objects.select_related().get(mirName__icontains=name)
    read_object= interval_object.read_alignment_set.filter(library__rescue__in=libraries).order_by('lib')
    len_count =read_object.values('read_length','library__rescue','read_counts','intervalName__sum_read_counts','normReads').annotate(Count('read_length')).order_by('read_length')
    lib_total_count =read_object.values('library__rescue').annotate(Sum('read_counts'))

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
        d[j['library__rescue']] = j['read_counts__sum']

       
    for i in len_count:
        # get variables as index and columns for dataframe. index being 'lh', col being 'lb'
        lb=i['library__rescue']
        lh=i['read_length']
        
        # This allows for choosing which way of normalizing    
        if normal == 'dist_rpm':
            data = i['read_length__count']*i['normReads']
            title = 'Reads per million'
           
        elif normal == 'dist_read_counts':
            data = i['read_length__count']*i['read_counts']
            title = 'Reads Counts'
        else: 
            data = (100*float(i['read_length__count']*i['read_counts']))/float(d[i['library__rescue']])
            title ='Read counts per miRNA mapped'
            
            # Fills the dataframe with values accessing using library id and read_length ** IMPORTANT
        df[lb][lh] += data
    
    # Draws the figure 
    fig= plt.figure(figsize=(8.27, 11.69), dpi=200)
    fig.set_facecolor("None")
    grid_size=(6,2) 
    ax1 = plt.subplot2grid(grid_size,(0,0),rowspan=4,colspan=2)
    graph = df.plot(ax=ax1 ,style=style,kind=chart_type,figsize=(10,8),subplots=False,legend=False)
    plt.title('Read Length Distribution of '+ str(interval_object.mirName))
    plt.xlabel('Length of Read')
    handles, labels = graph.get_legend_handles_labels()
    #graph.legend(handles, labels)
    graph.legend(handles,[i+' '+str(df[i].sum().round(2)) for i in libraries], title= 'Library : Total ',loc='best')

    plt.grid(True)
    plt.ylabel(title)
    plt.tight_layout()
    
    # Adds in the coordinates
    
    cord_df = df.max(axis=1).reset_index(0)
    cord_df['z']= cord_df[0]

    ## only generate labels for points that have at least 15% of the max value, to reduce labels and prevent cluttering of labels
    min_label = cord_df.max()[0] * 0.15
    cord_arr = np.array(cord_df)
    cord_tup = (map(tuple,cord_arr))
    
    for i in cord_tup:
        if i[1] == 0:
            pass
        elif i[2] < min_label:
            pass        
        else:
            if i[2] % 1 == 0:
               num = int(i[2])
            else:
                num = "%.2f"%i[2]
            plt.annotate(num , (int(i[0]),int(i[1])), xytext=(int(i[0]),int(i[1])), fontsize=12)
            
    # Generates the tables of values using the 2 plot spaces ax2, ax3
    df_round = np.round(df,2)        
    tex = df_round.to_latex(na_rep='').replace('\n', ' ')

    ax2 = plt.subplot2grid(grid_size,(4,0))
    ax2.axis('off')
    at = AnchoredText(tex,
        prop=dict(size=8), frameon=False,
                  loc=1,  bbox_to_anchor=(0.8,1.0), bbox_transform=ax2.transAxes)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax2.add_artist(at)

    ax3 = plt.subplot2grid(grid_size,(4,1))
    ax3.axis('off')
    summ = np.round(df.describe(),2)
    summary = summ.to_latex(na_rep='').replace('\n', ' ')
    at2 = AnchoredText(summary,
        prop=dict(size=8), frameon=False,
                  loc=1,  bbox_to_anchor=(0.9,1.0), bbox_transform=ax3.transAxes)
    at2.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax2.add_artist(at2)

    canvas = FigureCanvas(fig)
    response = HttpResponse(mimetype='image/jpg')
    fig.savefig(response, format='png')
    canvas.print_png(response)
    return response



def Graph_Form(request):
    """Generates a page for a form for user selection to generate plots"""
    ## See forms.py for list of fields that is used in this form. exceptions are caught using try/except commands as shown below
    errors = []
    # makes sure that the user is logged in to be able to do anything 
    if request.user.is_authenticated():
        
        if request.method == 'POST':
            # Throws an error if the miRNA name field is blank
            if not request.POST.get('mirName',''):
                errors.append("Enter a miRNA name")
                #Gets form data from POST and cleans it for usage
            form = GraphForm(request.POST)
            if form.is_valid():         
                name= form.cleaned_data['mirName']
                libraries = form.cleaned_data['Library']
                chart_type = form.cleaned_data['Chart']
                # Tells what kind of plot it is, line plots have special options like style that bar charts don't have
                if chart_type == 'line':
                    style = 'o-'
                else :
                    style = None
                normal = form.cleaned_data['Normal']
                try:
                    #tries to generate a response page with the plots plus variables from the form
                    response =  plot_graph(name,libraries,chart_type,normal,style)
                    return response 
                    
                    # if more than one miRNA is found when searching for the mirName, throw this error
                except (MultipleObjectsReturned), e :
                    return HttpResponse("Please provide a specific query. Your search returned more than one result.")
                # throws error when search returns no results 
                except ObjectDoesNotExist:
                    return HttpResponse("Please check your query, the miRNA does not exist in the database.")
            else:
                ## gets data from redirect from interval detail page, using the previous mirName for data
                form = GraphForm()
                if request.GET['url']:
                    interval_id= request.GET['url'].split('/')[1]
                    name = Interval.objects.get(id=int(interval_id)).mirName
                    try:
                        form.fields['mirName'].initial = name
                    except KeyError:
                        pass
                    # throws error if form is not entirely filled up
                errors.append('Please choose all the fields before selecting')
                return render(request,'loq/graph_filter.html',{'form':form,'errors':errors })
                
        else:
            form = GraphForm()
            #errors.append('Please choose all the fields before selecting')
            return render(request,'loq/graph_filter.html',{'form':form,'errors':errors })
    else:
        return HttpResponseRedirect('/login/')
