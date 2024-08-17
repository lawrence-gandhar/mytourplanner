from datetime import datetime

from django.db.models import F

from app.models import (
    TourData,
    TravelMode,
    TravelModeCost,
    TollData,
    ViaStops,
    StayData,
    StopsData
)

def get_tourdata(id=None):
    try:
        result = TourData.objects.get(pk=id)
        return result
    except:
        return None
    

def fetch_tourdata(user_id, limit=None, page=None, **kwargs):
    result = TourData.objects.filter(
        user_id = user_id
    )
    return result


def fetch_planned_tours(queryset=None):
    result = queryset.filter(
            travel_start_date__isnull = True
        ).values(
            'id', 'created_on', 'plan_to_start_on', 'travel_start_date', 
            'travel_end_date', 'source', 'destination', 'put_on_hold'
        )
    return result


def fetch_completed_tours(queryset=None):
    result = queryset.filter(
            travel_end_date__isnull = False
        ).values(
            'id', 'created_on', 'plan_to_start_on', 'travel_start_date', 
            'travel_end_date', 'source', 'destination'
        )
    return result


def fetch_calendar_data(queryset=None, start_date=None, end_date=None):
    result = queryset.select_related("tour_data").filter(
            created_on__gte =  start_date,
            created_on__lte = end_date
        ).values(
            'id', 'created_on', 'plan_to_start_on', 'travel_start_date', 'travel_end_date', 'source', 'destination', 
            'planned_no_days', 'tour_data__travel_mode', 'tour_data__travel_class_type', 
            'tour_data__no_of_adults', 'tour_data__no_of_children',travel_source=F('tour_data__source'), 
            travel_destination=F('tour_data__destination')
        )
    return result


def fetch_tour_counters(user_id=None):
    result = TourData.objects.filter(
        user_id = user_id
    ).values(
        'id', 'created_on', 'plan_to_start_on', 'travel_start_date', 'travel_end_date', 
        'source', 'destination', 'budget', 'put_on_hold',
        'total_spent'
    )
    return result


def fetch_travelmode_data(travel_mode_id=None, tour_data_id=None):
    
    queryset = TravelMode.objects.select_related('travelmode_cost').all()

    if tour_data_id:
        queryset = queryset.filter(
            tour_id = int(tour_data_id)
        ).values(
            'travel_date', 'travel_mode', 'travel_class_type', 
            'source', 'destination', 'distance', 'no_of_adults',
            'no_of_children', 'vendor', 'total_cost', 'discount',
            'gst', 'travelmode_cost__cost_per_adult',
            'travelmode_cost__cost_per_child'
        ) 
    
    if travel_mode_id:
        queryset = queryset.filter(
            tour_id = int(travel_mode_id)
        ).values(
            'travel_date', 'travel_mode', 'travel_class_type', 
            'source', 'destination', 'distance', 'no_of_adults',
            'no_of_children', 'vendor', 'total_cost', 'discount',
            'gst', 'travelmode_cost__cost_per_adult',
            'travelmode_cost__cost_per_child'
        )  
    return queryset

    
