from datetime import datetime

from app.models import (
    TourData,
    TollData,
    ViaStops,
    StayData,
    StopsData
)

def fetch_tourdata(user_id, limit=None, page=None, **kwargs):
    queryset = TourData.objects.filter(
        user_id = user_id
    )

    return queryset
