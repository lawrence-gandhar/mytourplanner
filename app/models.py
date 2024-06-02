from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class TourData(models.Model):

    travel_date = models.DateField(
        auto_now = False, 
        auto_now_add = False, 
        blank = True, 
        null = True, 
        db_index = True
    )

    plan_to_start_on = models.DateField(
        auto_now = False,
        auto_now_add = False,
        null = True,
        blank = True,
        db_index = True,
    )

    source = models.CharField(
        null = False,
        blank = False,
        db_index = True,
        max_length = 250
    )

    destination = models.CharField(
        null = False,
        blank = False,
        db_index = True,
        max_length = 250
    )

    created_on = models.DateTimeField(
        auto_now_add = True,
        auto_now = False,
        db_index = True
    )

    modified_on = models.DateTimeField(
        auto_now = True,
        auto_now_add = False,
        db_index = True
    )

    budget = models.DecimalField(
        decimal_places = 2,
        db_index = True,
        default = 0.00,
        max_digits = 10,
    )

    put_on_hold = models.BooleanField(
        default = False,
        db_index = True
    )

    no_of_heads =  models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
    )

    reviews = models.TextField(
        null = True,
        blank = True
    )

    road_reviews = models.TextField(
        null = True,
        blank = True
    )

    traffic_reviews = models.TextField(
        null = True,
        blank = True
    )

# Extended Tour

class ExtendedTour(models.Model):
    tour = models.ForeignKey(
        TourData,
        db_index = True,
        on_delete = models.CASCADE,
        null = False,
        blank = True
    )

    ext_destination = models.CharField(
        null = False,
        blank = False,
        db_index = True,
        max_length = 250
    )

    start_date =  models.DateField(
        auto_now = False,
        auto_now_add = False,
        null = True,
        blank = True,
        db_index = True,
    )

    end_date =  models.DateField(
        auto_now = False,
        auto_now_add = False,
        null = True,
        blank = True,
        db_index = True,
    )

    reviews = models.TextField(
        null = True,
        blank = True
    )


# ViaStops will have possible stop details between the TourData source and Destination
class ViaStops(models.Model):

    tour = models.ForeignKey(
        TourData,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True
    )

    halt_name = models.CharField(
        null = False,
        blank = False,
        db_index = True,
        max_length = 250   
    )

    place = models.CharField(
        null = False,
        blank = False,
        db_index = True,
        max_length = 250
    )

    halt_stop_on = models.DateField(
        auto_now = False,
        auto_now_add = False,
        null = True,
        blank = True,
        db_index = True,
    )

    halt_start_on = models.DateField(
        auto_now = False,
        auto_now_add = False,
        null = True,
        blank = True,
        db_index = True,
    )

    next_planned_stop = models.CharField(
        null = True,
        blank = True,
        db_index = True,
        max_length = 250
    )

# Stops
class StopsData(models.Model):

    HALT_CHOICES = (
        ("1", "TEA/MEALS/DRINKS"),
        ("2", "WASHROOM"),
        ("3", "GAS REFILL"),
        ("4", "TOLL"),
        ("5", "STAY"),
        ("6", "BREAK"),
        ("7", "LAYOVER/CHANGE STOPS"),
        ("8", "SIGHTSEEING/LEISURE"),
    )

    HALT_AT = (
        ("1", "ROADSIDE"),
        ("2", "TOLL BOOTH"),
        ("3", "GAS STATION"),
        ("4", "MALL"),
        ("5", "HOTEL"),
        ("6", "SIGHTSEEING/LEISURE"),
        ("7", "AIRPORT"),
        ("8", "TRAIN STATION"),
        ("9", "BUS STOP")
    )

    tour = models.ForeignKey(
        TourData,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True
    )

    tour_source = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = True
    )

    tour_destination = models.CharField(
        max_length = 250,
        db_index = True,
        null = True,
        blank = True
    )

    tour_start_date = models.DateTimeField(
        auto_now = False,
        auto_now_add = False,
        db_index = True,
        null = True,
        blank = True
    )

    tour_end_date = models.DateTimeField(
        auto_now = False,
        auto_now_add = False,
        db_index = True,
        null = True,
        blank = True
    )

    halt_type = models.CharField(
        max_length = 1,
        default = 1,
        db_index = True,
        choices = HALT_CHOICES
    )

    halt_at = models.CharField(
        max_length = 1,
        default = 1,
        db_index = True,
        choices = HALT_CHOICES
    )
    
    halt_name = models.CharField(
        null = False,
        blank = False,
        db_index = True,
        max_length = 250   
    )

    latitude = models.DecimalField(
        null = True,
        blank = True,
        db_index = True,
        max_digits = 10,
        decimal_places = 5  
    )

    longitude = models.DecimalField(
        null = True,
        blank = True,
        db_index = True,
        max_digits = 10,
        decimal_places = 5  
    )

    place = models.CharField(
        null = False,
        blank = False,
        db_index = True,
        max_length = 250
    )

    halt_stop_on = models.DateField(
        auto_now = False,
        auto_now_add = False,
        null = True,
        blank = True,
        db_index = True,
    )

    halt_start_on = models.DateField(
        auto_now = False,
        auto_now_add = False,
        null = True,
        blank = True,
        db_index = True,
    )

    reviews = models.TextField(
        blank = True,
        null = True
    )


# Hotels and Stay
class StayData(models.Model):

    stopsdata = models.ForeignKey(
        StopsData,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True
    )

    place = models.CharField(
        null = False,
        blank = False,
        db_index = True,
        max_length = 250
    )

    has_free_wifi = models.BooleanField(
        default = False,
        db_index = True
    )

    breafast_included = models.BooleanField(
        default = False,
        db_index = True
    )

    lunch_included = models.BooleanField(
        default = False,
        db_index = True
    )

    dinner_included = models.BooleanField(
        default = False,
        db_index = True
    )

    ac_working = models.BooleanField(
        default = False,
        db_index = True
    )

    is_clean = models.BooleanField(
        default = False,
        db_index = True
    )

    has_attached_washroom = models.BooleanField(
        default = False,
        db_index = True
    )

    has_cupboards = models.BooleanField(
        default = False,
        db_index = True
    )

    provides_toiletery = models.BooleanField(
        default = False,
        db_index = True
    )

    has_balcony = models.BooleanField(
        default = False,
        db_index = True
    )

    tv_working = models.BooleanField(
        default = False,
        db_index = True
    )

    smoking_area = models.BooleanField(
        default = False,
        db_index = True
    )

    prompt_service = models.BooleanField(
        default = False,
        db_index = True
    )

    hot_water = models.BooleanField(
        default = False,
        db_index = True
    )

    has_resturant = models.BooleanField(
        default = False,
        db_index = True
    )

    cost = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        db_index = True,
        default = 0.00,
    )

    no_of_rooms = models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
    )

    no_of_adults = models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
    )

    no_of_nights = models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
    )

    place_reviews = models.TextField(
        null = True,
        blank = True
    )

    place_rating = models.IntegerField(
        null = True,
        blank = True,
        default = 0,
        db_index = True
    )

    room_review = models.TextField(
        null = True,
        blank = True
    )

    room_rating = models.IntegerField(
        default = 0,
        db_index = True,
        blank = True,
        null = True
    )

    service_reviews = models.TextField(
        null = True,
        blank = True
    )

    service_rating = models.IntegerField(
        default = 0,
        db_index = True,
        blank = True,
        null = True
    )

    food_review = models.TextField(
        null = True,
        blank = True
    )

    food_rating = models.IntegerField(
        default = 0,
        db_index = True
    )

    complete_review = models.TextField(
        null = True,
        blank = True
    )

    review_rating = models.IntegerField(
        default = 0,
        db_index = True
    )

    value_for_location = models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
    )

    value_for_cost = models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
    )

    should_visit_again = models.BooleanField(
        default = False,
        db_index = True
    )


# Tolls Entry
class TollData(models.Model):

    stopsdata = models.ForeignKey(
        StopsData,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True
    )

    latitude = models.DecimalField(
        null = True,
        blank = True,
        db_index = True,
        max_digits = 10,
        decimal_places = 5  
    )

    longitude = models.DecimalField(
        null = True,
        blank = True,
        db_index = True,
        max_digits = 10,
        decimal_places = 5  
    )

    place = models.CharField(
        null = False,
        blank = False,
        db_index = True,
        max_length = 20  
    )

    budget = models.DecimalField(
        decimal_places = 2,
        db_index = True,
        default = 0.00,
        max_digits = 10,
    )

    is_fast_tag = models.BooleanField(
        default = False,
        db_index = True
    )

    stop_time = models.IntegerField(
        default = 0,    
        null = False,
        blank = False,
        db_index = True,
    )

    fees = models.DecimalField(
        decimal_places = 2,
        db_index = True,
        default = 0.00,
        max_digits = 10
    )

    reviews = models.TextField(
        null = True,
        blank = True
    )

    review_rating = models.IntegerField(
        default = 0,
        db_index = True
    )

    road_reviews = models.TextField(
        null = True,
        blank = True
    )

    road_rating = models.IntegerField(
        default = 0,
        db_index = True
    )

    traffic_reviews = models.TextField(
        null = True,
        blank = True
    )

    traffic_rating = models.IntegerField(
        default = 0,
        db_index = True
    )


# Meals data
class MealsData():

    MEALS_CHOICES = (
        ("1", "TEA"),
        ("2", "BREAKFAST"),
        ("3", "BRUNCH"),
        ("4", "LUNCH"),
        ("5", "SNACKS"),
        ("6", "DINNER"),
        ("7", "DRINKS")
    )

    stopsdata = models.ForeignKey(
        StopsData,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True
    )

    meal_type = models.CharField( 
        max_length = 1, 
        choices = MEALS_CHOICES, 
        default = '1',
        db_index = True
    ) 

    cost = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        db_index = True,
        default = 0.00,
    )
   


