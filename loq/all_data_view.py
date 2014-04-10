from django.shortcuts import render
from io import BytesIO
from loq.tables import AlignTable
from django_tables2 import RequestConfig
from loq.models import Read_alignment, AlignFilter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

#page for table with alignments, intervals of all data

def align(request):
    table= AlignTable(Read_alignment.objects.all().order_by('strand','id'))
    RequestConfig(request).configure(table)
    return render(request,"align_data.html",{'all_data':table})

def align_filter(request):
    aln = AlignFilter(request.GET, queryset = Read_alignment.objects.select_related().all())
    al= AlignTable(aln.qs)
    RequestConfig(request).configure(al)
    return render(request,'align_filter.html', {'al': al, 'aln':aln})
    
def view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="file.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100,100,"text.")
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
