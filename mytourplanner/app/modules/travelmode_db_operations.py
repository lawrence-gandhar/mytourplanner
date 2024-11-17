from django.db.models import Value, F
from django.db.models.functions import Concat, Upper

from app.models import TravelMode
from app.modules import custom_constants as cs

# =====================================================
# Fetch Travel Mode Data
# =====================================================
def fetch_travelmode_data(travel_mode_id=None, tour_data_id=None, user_id=None):
    
    queryset = TravelMode.objects.select_related('travelmode_cost').all()

    if tour_data_id:
        queryset = queryset.filter(
            tour_id = int(tour_data_id)
        )

    if travel_mode_id:
        queryset = queryset.filter(
            id = int(travel_mode_id)
        )

    if user_id:
        queryset = queryset.filter(
            user_id = int(user_id)
        ) 
    
    queryset = queryset.values(
            'travel_date', 'travel_mode', 'travel_class_type', 
            'source', 'destination', 'distance', 'no_of_adults',
            'no_of_children', 'vendor', 'total_cost', 'discount',
            'gst', 'travelmode_cost__cost_per_adult',
            'travelmode_cost__cost_per_child'
        ) 
     
    return queryset

# =====================================================
# Fetch Travel Modes
# =====================================================
def fetch_travel_modes(tour_data_id):
    queryset = TravelMode.objects.annotate(
        from_to = Concat(
            Upper('source'),
            Value(' - '),
            Upper('destination')
        )
    ).filter(tour_id=tour_data_id).values('id','travel_mode', 'from_to')

    print(queryset)

    return queryset
