import django_tables2 as tables
from django_tables2 import SingleTableMixin
from django_tables2.utils import A
from django.db.models import Avg
from models import Interval, Read_alignment
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from favit.models import Favorite

class UserTable(SingleTableMixin,tables.Table):
    class Meta:
        model = User
        attrs = {"class":"paleblue"}
        fields =('username','email','last_login','is_staff')
        
class FavTable(SingleTableMixin,tables.Table):
    mirna = tables.LinkColumn('IntervalDetailView',args=[A('target.pk')],accessor="target.mirName", verbose_name="miRNA")
    class Meta:
        model = Favorite
        attrs = {"class":"paleblue"}
        fields =('timestamp',)
        sequence =('mirna','timestamp') 
class CommentTable(SingleTableMixin,tables.Table):
    mirna = tables.LinkColumn('IntervalDetailView',args=[A('content_object.pk')],accessor="content_object.mirName", verbose_name="miRNA")
    class Meta:
        model = Comment
        attrs = {"class":"paleblue"}
        fields =('comment','submit_date')
        sequence=('mirna','comment','submit_date')
    
class IntervalTable(tables.Table):
     mirName = tables.LinkColumn('IntervalDetailView',args=[A('pk')])
     chr=tables.Column(verbose_name='Chromosome')
     Link = tables.TemplateColumn('<a href="{{record.Link}}">View</a>')
     class Meta:
        model = Interval
        attrs = {"class":"paleblue"}
        order_by = ('id',)
        fields =('mirName','NeatName','chr','start','stop','mapped_strand','IntervalSize','sum_read_counts','sum_normReads','Link')

        # link column. name = " ", " " = AlignDetailView

class IntervalTable1(tables.Table):
     mirName = tables.LinkColumn('IntervalDetailView',args=[A('pk')])
     chr=tables.Column(verbose_name='Chromosome')
     class Meta:
        model = Interval
        attrs = {"class":"paleblue"}
        fields=('mirName','NeatName', 'chr','start','stop','mapped_strand','IntervalSize','sum_read_counts')
 
class AlignTable(tables.Table):
    #id= tables.CheckBoxColumn()
    # table cannot be sorted by normRead
    # intervalName = tables.Column(order_by=('intervalName'))
    id = tables.LinkColumn('AlignDetailView',args=[A('pk')])
    library__rescue= tables.Column(verbose_name='Library')
    class Meta:
        model = Read_alignment
        sequence = ('id','chr','start','stop','sequence','normReads','genomic_hits','strand','library__rescue','read_length')
        fields=('id','chr','start','stop','sequence','normReads','genomic_hits','strand','library__rescue','read_length')
        attrs = {"class":"paleblue"}
        order_by = ('lib','strand')
        

class DetailTable(SingleTableMixin,tables.Table):
    class Meta:
        model = Read_alignment
        sequence = ('chr','start','stop','strand','read_counts','genomic_hits','normReads','sequence','read_length')
        attrs = {"class":"paleblue"}
        fields=('lib','chr','start','stop','read_counts','genomic_hits','strand','normReads','sequence','read_length')
       

#table_data = (Read_alignment.objects.get(id='127'))
#class IntervalDetailTable(SingleTableMixin,tables.Table):
