from django import forms
from app.models import TourData


class TourDataInitialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form_fields'
            self.fields["put_on_hold"].widget.attrs.update({"class": "form-check-input form_fields"})

    class Meta:
        model = TourData
        fields = [
            "plan_to_start_on", "planned_no_days", "source", "destination",
            "budget", "put_on_hold", "no_of_adults", "no_of_children",
        ]
        widgets = {
            "plan_to_start_on": forms.DateInput(attrs={'class':'form-control', 'type':'date', 'required':True}),
        }
    
class TourNextForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form_fields'
            
    class Meta:
        model = TourData
        fields = [
            "travel_start_date", "budget"  
        ]
        widgets = {
            "travel_start_date": forms.DateInput(attrs={'class':'form-control', 'type':'date', 'required':True}),
            "budget": forms.NumberInput(attrs={'class':'form-control', 'type':'number', 'required':True}),
        }


class TourDataUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form_fields'
            self.fields["put_on_hold"].widget.attrs.update({"class": "form-check-input form_fields"})

    class Meta:
        model = TourData
        fields = [
            "id", "plan_to_start_on", "travel_start_date", "source", "destination", "budget", 
            "put_on_hold", "no_of_adults", "no_of_children", "reviews", "road_reviews", 
            "traffic_reviews", "overall_road_rating", "overall_tour_rating", 
            "total_spent", "visit_again", "planned_no_days", "travel_end_date" 
        ]
        widgets = {
            "plan_to_start_on": forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            "travel_start_date": forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }
    