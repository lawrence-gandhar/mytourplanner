from datetime import datetime

from app.models import (
    TourData,
    TollData,
    ViaStops,
    StayData,
    StopsData
)

def get_tourdata(id=None):
    result = TourData.objects.prefetch_related('travelmode_set').get(pk=id)
    print(result)
    return result
    # try:
    #     result = TourData.objects.prefetch_related('tourdata__travelmode').get(pk=id)
    #     print(result.query)
    #     return result
    # except:
    #     return None

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


def fetch_tour_counters(user_id=None):
    result = TourData.objects.filter(
        user_id = user_id
    ).values(
        'id', 'created_on', 'plan_to_start_on', 'travel_start_date', 'travel_end_date', 
        'source', 'destination', 'budget', 'put_on_hold',
        'total_spent'
    )
    return result


