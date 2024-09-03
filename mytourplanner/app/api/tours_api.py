from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import (
    TourData,
    TollData,
    ViaStops,
    StayData,
    StopsData
)

import app.modules.db_operations as dbops

class ListPlannedTours(APIView):

    def get(self, request):
        data = {}

        queryset = dbops.fetch_tourdata(request.user)
        data = dbops.fetch_planned_tours(queryset=queryset)

        return Response(data)
