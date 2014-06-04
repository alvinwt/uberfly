from django.views.generic.list import ListView
from django_tables2 import RequestConfig, SingleTableMixin
from django.shortcuts import render
from tables import IntervalTable, IntervalTable1
from loq.models import Interval, IntervalFilter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

"""Generates the homepage usings Django class-based views, listview and the django-tables2 single table mixin

IntervalList is the class based view way of writing a page that generates a list rendered in a table
"""
class IntervalList(SingleTableMixin,ListView):
     model = Interval
     table_class = IntervalTable
     table_pagination ={'per_page':20}

     # Django method to require login access to the page 
     @method_decorator(login_required)
     def dispatch(self, *args, **kwargs):
         return super(IntervalList,self).dispatch(*args, **kwargs)

# login required is used in functional based views as belows. 
@login_required
def int_filter(request):
    fil = IntervalFilter(request.GET, queryset = Interval.objects.select_related().all())
    # retrieves the queryset from the Intervalfilter and renders it as a table
    f= IntervalTable1(fil.qs)
    RequestConfig(request).configure(f)
    return render(request,'loq/filter.html', {'f': f, 'fil':fil})
