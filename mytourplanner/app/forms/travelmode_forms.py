from django import forms
from app.models import TravelMode, TravelModeCost

from app.modules import custom_constants as cs

class TravelModeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form_fields'
            
    class Meta:
        model = TravelMode
        fields = [
            'travel_mode', 'source', 'destination', 'distance', 'no_of_adults', 'no_of_children', 'total_cost', 'gst'
        ]
        widgets = {
            "travel_mode": forms.Select(attrs={'class':'form-control'}, choices=cs.TRAVELMODE_CHOICES),
        }


class TravelModeCostCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form_fields'

    class Meta:
        model = TravelModeCost
        fields = [
            'cost_per_adult', 'cost_per_child', 'travel_class_type'
        ]
        widgets = {
            "travel_class_type": forms.Select(attrs={'class':'form-control'}),
        }

