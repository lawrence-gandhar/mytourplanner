from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response


import app.modules.tourdata_db_operations as tourdata_dbops

class ListPlannedTours(APIView):

    def get(self, request):
        data = {}

        queryset = tourdata_dbops.fetch_tourdata(request.user)
        data = tourdata_dbops.fetch_planned_tours(queryset=queryset)

        return Response(data)
