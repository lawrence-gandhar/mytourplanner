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
            'travel_mode', 'source', 'destination', 'travel_date', 'distance', 'no_of_adults', 
            'no_of_children', 'total_cost', 'gst', 'vendor', 'discount', 'travel_class_type'
        ]
        widgets = {
            "source": forms.TextInput(attrs={'required':True}),
            "destination": forms.TextInput(attrs={'required':True}),
            "distance": forms.NumberInput(attrs={'required':True}),
            "travel_mode": forms.Select(choices=cs.TRAVELMODE_CHOICES),
            "travel_date": forms.DateInput(attrs={'type':'date', 'required':True}),
            "no_of_children": forms.NumberInput(attrs={'onfocusout':'get_total_amount()'}),
            "no_of_adults": forms.NumberInput(attrs={'onfocusout':'get_total_amount()'}),
            "gst": forms.NumberInput(attrs={'onfocusout':'get_total_amount()'}),
            "total_cost": forms.NumberInput(attrs={'readonly':True}),
            "discount": forms.NumberInput(attrs={'onfocusout':'get_total_amount()'}),
            "travel_class_type": forms.Select(attrs={'class':'form-control'}),
        }


class TravelModeCostCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form_fields'

    class Meta:
        model = TravelModeCost
        fields = [
            'cost_per_adult', 'cost_per_child', 
        ]
        widgets = {
            "cost_per_adult": forms.NumberInput(attrs={'onfocusout':'get_total_amount()'}),
            "cost_per_child": forms.NumberInput(attrs={'onfocusout':'get_total_amount()'}),
        }

