from django import forms
from loq.models import Library

""" Forms.py generates the form for the read length distribution generator.
Each variable is a form field that can be either a charfield, multiple/checkbox or choice field. For more information on the form fields pls refer to Django 1.5 documentation https://docs.djangoproject.com/en/1.5/ref/forms/fields/.
"""

class GraphForm(forms.Form):
    # Retrieves a list of libraries for selection in the form
    libs = Library.objects.all().values_list('rescue',flat=True)
    choice =[]
    for i in libs:
        choice.append((i,i))
        
    mirName = forms.CharField(max_length=100, label='miRNA Name',
                              help_text="You can exclude 'dme-mir', but do provide a specific name e.g. 307a.",
                              initial='dme-bantam')
    
    Library = forms.MultipleChoiceField(required=True,
                                        widget=forms.CheckboxSelectMultiple,
                                        choices=choice,initial=libs,
                                        help_text="Check or uncheck boxes to select which library values are used for the analysis.")
    
    Chart= forms.ChoiceField(required=True, label= "Chart type",
                             choices=[('bar','Bar'),('line','Line')],
                             help_text="Select either bar or chart output format.")
    
    Normal= forms.ChoiceField(required=True, label= "Normalization",
                              choices=[('dist_read_counts','Raw Read Count'),('dist_rpm','Reads Per Million'),('dist_percent_read_counts','Percentage miRNA Mapped')],
                              help_text="Choose the method of normalizing the values used for analysis.")  
