from django.db.models import F, DateField,  ExpressionWrapper, Q
from app.models import TourData


# =====================================================
# Fetch TourData based on id
# =====================================================
def get_tourdata(id=None):
    try:
        result = TourData.objects.get(pk=id)
        return result
    except:
        return None
    
# =====================================================
# Fetch TourData based on user id
# =====================================================
def fetch_tourdata(user_id, limit=None, page=None, **kwargs):
    result = TourData.objects.filter(
        user_id = user_id
    )
    return result


# =====================================================
# Fetch Planned Tours
# =====================================================
def fetch_planned_tours(queryset=None):
    result = queryset.filter(
            travel_end_date__isnull = True
        ).annotate(
            planned_till=ExpressionWrapper(
                F('plan_to_start_on') + F('planned_no_days'), 
                output_field=DateField()
            )
        ).values(
            'id', 'created_on', 'plan_to_start_on', 'travel_start_date', 
            'travel_end_date', 'source', 'destination', 'put_on_hold', 'planned_no_days', 'planned_till',
            'cancelled', 'modified_on'
        )
    return result


# =====================================================
# Fetch Completed Tours
# =====================================================
def fetch_completed_tours(queryset=None):
    result = queryset.filter(
            travel_end_date__isnull = False
        ).values(
            'id', 'created_on', 'plan_to_start_on', 'travel_start_date', 
            'travel_end_date', 'source', 'destination'
        )
    return result


# =====================================================
# Fetch Calendar Data
# =====================================================
def fetch_calendar_data(queryset=None, start_date=None, end_date=None):
    result = queryset.select_related("tour_data").filter(
            Q (
                (Q(plan_to_start_on__gte = start_date) & Q(plan_to_start_on__lte = end_date)) | 
                (Q(travel_start_date__gte = start_date) & Q(travel_start_date__lte = end_date))
            )
        ).values(
            'id', 'created_on', 'plan_to_start_on', 'travel_start_date', 'travel_end_date', 'source', 'destination', 
            'planned_no_days', 'tour_data__travel_mode', 'tour_data__travel_class_type', 'tour_data__travel_date',
            'tour_data__source', 'tour_data__destination',
            'tour_data__no_of_adults', 'tour_data__no_of_children',travel_source=F('tour_data__source'), 
            travel_destination=F('tour_data__destination')
        )
    
    return result


# =====================================================
# Fetch Tour Counters
# =====================================================
def fetch_tour_counters(user_id=None):
    result = TourData.objects.filter(
        user_id = user_id
    ).values(
        'id', 'created_on', 'plan_to_start_on', 'travel_start_date', 'travel_end_date', 
        'source', 'destination', 'budget', 'put_on_hold',
        'total_spent'
    )
    return result



