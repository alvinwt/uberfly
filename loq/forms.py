from django import forms
from loq.models import Library

class GraphForm(forms.Form):
    libs = Library.objects.all().values_list('rescue',flat=True)
    choice =[]
    for i in libs:
        choice.append((i,i))
        
    mirName = forms.CharField(max_length=100,label='miRNA Name',help_text="You can exclude 'dme-mir', but do provide a specific name e.g. 307a.", initial='dme-bantam')
    Library = forms.MultipleChoiceField(required=True,
                                        widget=forms.CheckboxSelectMultiple, choices=choice,initial=libs,help_text="Check or uncheck boxes to select which library values are used for the analysis.")
    Chart= forms.ChoiceField(required=True, label= "Chart type", choices=[('bar','Bar'),('line','Line')],help_text="Select either bar or chart output format.")
    Normal= forms.ChoiceField(required=True, label= "Normalization", choices=[('dist_read_counts','Raw Read Count'),('dist_rpm','Reads Per Million'),('dist_percent_read_counts','Percentage miRNA Mapped')],help_text="Choose the method of normalizing the values used for analysis.")
     
    # def create_graph(self,form):
    #     if form.is_valid():
    #         pk = self.cleaned_data.get('id')
    #         selected_interval = Interval.objects.get(id=pk).values('chr','start','stop')
    #         pass
        #return pk
    #     object = Interval.objects.select_related().get(chr=self.chr,start=self.start,stop=self.stop,mirName=self.mirName)
    #     object= object.values('mirName','read_alignment__read_length','read_alignment__read-counts')
    #     return object 
