from django.views.generic.list import ListView
from django_tables2 import RequestConfig, SingleTableMixin
from django.shortcuts import render
from tables import IntervalTable, AlignTable, IntervalTable1
from loq.models import Interval, IntervalFilter,Read_alignment, AlignFilter
from django.shortcuts import render_to_response
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class IntervalList(SingleTableMixin,ListView):
     model = Interval
     table_class = IntervalTable
     table_pagination ={'per_page':20}

     @method_decorator(login_required)
     def dispatch(self, *args, **kwargs):
         return super(IntervalList,self).dispatch(*args, **kwargs)

@login_required
def int_filter(request):
    fil = IntervalFilter(request.GET, queryset = Interval.objects.select_related().all())
    f= IntervalTable1(fil.qs)
    RequestConfig(request).configure(f)
    return render(request,'loq/filter.html', {'f': f, 'fil':fil})

# def IntervalList(request):
#     intTable= IntervalTable(Interval.objects.all())
#     RequestConfig(request).configure(intTable)
#     return render(request,"interval_list.html",{'table':intTable})


# def search_form(request):
#     if request.method == 'GET':
#         form = MyModelForm(request.GET)
#         if form.is_valid():
#             return render(request,'loq/int_data.html')
#         else:
#             return "error, template not found"

        # class HomeView(TemplateView):
#     template_name = "srb/home.html"
#     #html not written yet
