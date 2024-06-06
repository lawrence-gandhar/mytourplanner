from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from app.models import TourData, ViaStops, StayData, StopsData, MealsData


class TourDataListSerializers(serializers.ModelSerializer):

    amount_per_head = serializers.SerializerMethodField()
    final_amount_per_head = serializers.SerializerMethodField()

    def get_amount_per_head(self, obj):
        return round(obj.budget/(obj.no_of_adults + obj.no_of_children), 2)

    def get_final_amount_per_head(self, obj):
        return round(obj.total_spent/(obj.no_of_adults + obj.no_of_children), 2)

    class Meta:
        model = TourData
        fields = (
            "plan_to_start_on", "travel_start_date", "source", "destination", "budget", 
            "put_on_hold", "no_of_adults", "no_of_children", "reviews", "road_reviews", 
            "traffic_reviews", "overall_road_rating", "overall_tour_rating", 
            "total_spent", "visit_again", "amount_per_head", "final_amount_per_head",
            "created_on", "modified_on" 
        )


class TourDataInitialSerializers(serializers.ModelSerializer):
    class Meta:
        model = TourData
        fields = (
            "plan_to_start_on", "travel_start_date", "source", "destination", "budget", 
            "put_on_hold", "no_of_adults", "no_of_children"
        )

    

class TourDataCompleteSerializers(serializers.ModelSerializer):
    
    actual_amount_spent_per_head = serializers.SerializerMethodField()

    def get_actual_amount_spent_per_head(self, obj):
        return round(obj.total_spent/(obj.no_of_adults + obj.no_of_children), 2)

    class Meta:
        model = TourData
        fields = (
            "reviews", "road_reviews", "traffic_reviews", "overall_road_rating", "overall_tour_rating", 
            "total_spent", "visit_again", "actual_amount_spent_per_head"
        )
