from django.forms import ModelForm
from django import forms
from app.models import TourData, ViaStops, StopsData, StayData, MealsData


class TourDataInitialForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form_fields'
            self.fields["put_on_hold"].widget.attrs.update({"class": "form-check-input form_fields"})

    class Meta:
        model = TourData
        fields = [
            "travel_start_date", "plan_to_start_on", "source", "destination",
            "budget", "put_on_hold", "no_of_adults", "no_of_children", "planned_no_days"
        ]
        widgets = {
            "plan_to_start_on": forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            "travel_start_date": forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }
    

    