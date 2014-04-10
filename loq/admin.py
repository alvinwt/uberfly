from django.contrib import admin
from loq.models import Library, Interval, Sequencing_Run, Read_alignment

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
    # ordering=('avg_counts')
#class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'publisher', 'publication_date')
#     list_filter = ('publication_date',)
#     date_hierarchy = ('publication_date')
#     ordering = ('-publication_date',)
#     # fields = ('title','authors','publisher',)
#     filter_horizontal = ('authors',)
#     raw_id_fields = ('publisher',)
    
admin.site.register(Library,LibAdmin)
admin.site.register(Sequencing_Run)
admin.site.register(Read_alignment,AlignmentAdmin)
admin.site.register(Interval,IntAdmin)
#admin.site.register(Author, AuthorAdmin)
