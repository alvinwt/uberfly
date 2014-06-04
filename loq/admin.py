from django.contrib import admin
from loq.models import Library, Interval, Sequencing_Run, Read_alignment

""" The admin.py file specifies the fields and search columns used in the Django admin interface.
This is entirely customizable to allow the admin interface GUI to search through database entries by name, id or user defined fields. Each admin interface below is for each database table: Library, Interval and Read_alignment. The register function links the classes to the admin interface GUI"""

class LibAdmin(admin.ModelAdmin):
    list_display = ('library_id',)
    search_fields = ('library_id',)

class IntAdmin(admin.ModelAdmin):
    list_display = ('IntervalSerialNumber','NeatName', 'chr','start','stop','mapped_strand','IntervalSize','mirName','Link','Tags','Annotations')
    search_fields =('NeatName','mirName' , 'IntervalSerialNumber','Tags','Annotations', 'chr','start','stop' )

class AlignmentAdmin(admin.ModelAdmin):
    search_fields =('id','chr', 'start','stop','lib','sequence',)
    list_display=('id','chr','start','stop','sequence','read_counts','intervalName','normReads','lib','genomic_hits','strand', 'read_length',
    #'library',
    )

admin.site.register(Library,LibAdmin)
admin.site.register(Sequencing_Run)
admin.site.register(Read_alignment,AlignmentAdmin)
admin.site.register(Interval,IntAdmin)
