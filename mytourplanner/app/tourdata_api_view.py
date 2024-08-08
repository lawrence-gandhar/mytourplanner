from app.serializers import (
    TourDataListSerializers, 
    TourDataInitialSerializers, 
    TourDataCompleteSerializers
)

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 

from django.http import JsonResponse, HttpResponse

from app.models import TourData


@api_view()
def tourdata_list(request):
    if request.method == 'GET': 
        queryset = TourData.objects.all()
        serializer = TourDataListSerializers(queryset, many = True)
        return JsonResponse(serializer.data, safe=False) 

@api_view()
def tourdata_latest(request):
    if request.method == 'GET': 
        queryset = TourData.objects.filter(travel_start_date__isnull = False).order_by("-id")[:5]
        serializer = TourDataListSerializers(queryset, many = True)
        return JsonResponse(serializer.data, safe=False)

@api_view()
def tourdata_planned(request):
    if request.method == 'GET': 
        queryset = TourData.objects.filter(
            travel_start_date__isnull = True, 
            plan_to_start_on__isnull = False,
        )[:5]

        serializer = TourDataListSerializers(queryset, many = True)
        return JsonResponse(serializer.data, safe=False)  


class TourPlanCreate(generics.ListCreateAPIView):
    queryset = TourData.objects.all()
    serializer_class = TourDataInitialSerializers


class TourPlanUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = TourData.objects.all()
    serializer_class = TourDataInitialSerializers


class TourComplete(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = TourData.objects.all()
    serializer_class = TourDataCompleteSerializers

