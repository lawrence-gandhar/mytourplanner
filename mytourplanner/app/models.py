from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from app.modules import custom_constants as cs

class TourData(models.Model):

    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        db_index = True,
        null=True,
        blank=True
    )

    travel_start_date = models.DateField(
        auto_now = False, 
        auto_now_add = False, 
        blank = True, 
        null = True, 
        db_index = True
    )

    travel_end_date = models.DateField(
        auto_now = False, 
        auto_now_add = False, 
        blank = True, 
        null = True, 
        db_index = True
    )

    planned_no_days =  models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
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

    cancelled = models.BooleanField(
        default = False,
        db_index = True
    )

    cancelled_due_to = models.TextField(
        null = True,
        blank = True,
    ) 

    no_of_adults =  models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
    )

    no_of_children =  models.IntegerField(
        default = 0,    
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

    overall_road_rating = models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
    )

    overall_tour_rating = models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
    )

    total_spent = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        db_index = True,
        default = 0.00,
    )

    visit_again = models.BooleanField(
        db_index = True,
        default = False
    )

    @property
    def plan_end_date(self):
        return self.plan_to_start_on + timedelta(days=self.planned_no_days) 

    class Meta:
        index_together = [
            ['travel_end_date', 'user'],
            ['created_on', 'user'],
            ['travel_start_date', 'travel_end_date', 'plan_to_start_on', 'user'],
            ['id', 'user', 'created_on'],
            ['id', 'created_on', 'plan_to_start_on', 'travel_start_date', 'travel_end_date', 
            'source', 'destination', 'planned_no_days', 'user'],
            ['id', 'created_on', 'plan_to_start_on', 'travel_start_date', 'travel_end_date', 
            'source', 'destination', 'planned_no_days', 'modified_on', 'budget', 'put_on_hold',
            'no_of_adults', 'no_of_children', 'overall_road_rating', 'overall_tour_rating',
            'total_spent', 'visit_again', 'user']
        ]

@receiver(pre_save, sender=TourData)
def tourdata_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        instance.source = instance.source.lower().strip()
        instance.destination = instance.destination.lower().strip()
        

# Travel Mode
class TravelMode(models.Model):

    user = models.ForeignKey(
        User,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True,
        blank = True
    )

    tour = models.ForeignKey(
        TourData,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "tour_data"
    )

    travel_date = models.DateField(
        db_index = True,
        null = True,
        blank = True
    )

    travel_mode = models.CharField(
        default = '1',
        db_index = True,
        max_length = 1,
        choices = cs.TRAVELMODE_CHOICES,
        null = False,
        blank = False
    )

    travel_class_type =  models.CharField(
        null = True,
        blank = True,
        db_index = True,
        max_length = 3
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

    distance = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        db_index = True,
        default = 0.00,
    )

    no_of_adults =  models.IntegerField(
        default = 1,    
        null = False,
        blank = False,
        db_index = True,
    )

    no_of_children =  models.IntegerField(
        default = 0,    
        null = False,
        blank = False,
        db_index = True,
    )

    vendor = models.CharField(
        null = True,
        blank = True,
        db_index = True,
        max_length = 250
    )

    total_cost = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        db_index = True,
        default = 0.00,
    )

    discount = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        db_index = True,
        default = 0.00,
    )

    gst = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        db_index = True,
        default = 0.00,
    )

    class Meta:
        index_together = [
            ['user', 'travel_mode', 'distance', 'total_cost', 'gst', 'discount'],
            ['tour', 'travel_mode', 'distance', 'total_cost', 'gst', 'discount'],
            ['user', 'tour', 'travel_mode', 'distance', 'total_cost', 'gst', 'discount']
        ]

# Travel Mode Class Type
class TravelModeCost(models.Model):
    
    travel_mode = models.ForeignKey(
        TravelMode,
        on_delete = models.SET_NULL,
        db_index = True,
        null = True,
        blank = True,
        related_name="travelmode_cost"
    ) 

    cost_per_adult = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        db_index = True,
        default = 0.00,
    )

    cost_per_child = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        db_index = True,
        default = 0.00,
    )

    class Meta:
        index_together = [
            'travel_mode', 'cost_per_adult', 'cost_per_child'
        ]

# Extended Tour
class ExtendedTour(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        db_index = True,
        null=True,
        blank=True
    )

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

    travel_mode = models.ForeignKey(
        TravelMode,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
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

@receiver(pre_save, sender=ExtendedTour)
def ext_tour_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        instance.ext_destination = instance.ext_destination.lower().strip()

# ViaStops will have possible stop details between the TourData source and Destination
class ViaStops(models.Model):

    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        db_index = True,
        null=True,
        blank=True
    )

    tour = models.ForeignKey(
        TourData,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True
    )

    travel_mode = models.ForeignKey(
        TravelMode,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
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
        db_index = True
    )

    next_planned_stop = models.ForeignKey(
        'self',
        null = True,
        blank = True,
        db_index = True,
        on_delete = models.SET_NULL
    )

    next_planned_skipped = models.BooleanField(
        default = False,
        db_index = True
    )

    next_planned_skipped_reason = models.TextField(
        null = True,
        blank = True
    )

@receiver(pre_save, sender=ViaStops)
def vaistops_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        instance.halt_name = instance.halt_name.lower().strip()
        instance.place = instance.place.lower().strip()
        instance.next_planned_stop = instance.halt_stop_on.lower().strip()
        instance.next_planned_skipped_reason = instance.next_planned_skipped_reason.lower().strip()


# Stops
class StopsData(models.Model):

    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        db_index = True,
        null=True,
        blank=True
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
        choices = cs.HALT_CHOICES
    )

    halt_at = models.CharField(
        max_length = 1,
        default = 1,
        db_index = True,
        choices = cs.HALT_AT
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

    stop_ratings = models.IntegerField(
        db_index = True,
        default = 1
    )

    has_washrooms = models.BooleanField(
        db_index = True,
        default = False
    )

    washroom_rating = models.IntegerField(
        db_index = True,
        default = 1
    ) 

    has_nursing_area = models.BooleanField(
        db_index = True,
        default = False
    )

    nursing_area_rating = models.IntegerField(
        db_index = True,
        default = 1
    ) 

    has_sitting_area = models.BooleanField(
        db_index = True,
        default = False
    )

    sitting_area = models.IntegerField(
        db_index = True,
        default = 1
    ) 

    has_drinking_water = models.BooleanField(
        db_index = True,
        default = False
    )

    has_smoking_area = models.BooleanField(
        db_index = True,
        default = False
    )

    has_ac = models.BooleanField(
        db_index = True,
        default = False
    )

    has_electricity = models.BooleanField(
        db_index = True,
        default = False
    )

    has_street_lights = models.BooleanField(
        db_index = True,
        default = False
    )

    safe_for_night_stop = models.BooleanField(
        db_index = True,
        default = False
    )

    has_localities_nearby = models.BooleanField(
        db_index = True,
        default = False
    )

@receiver(pre_save, sender=StopsData)
def stopsdata_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        instance.halt_name = instance.halt_name.lower().strip()
        instance.place = instance.place.lower().strip()
        instance.tour_source = instance.tour_source.lower().strip()
        instance.tour_destination = instance.tour_destination.lower().strip()
        instance.reviews = instance.reviews.lower().strip()



# Hotels and Stay
class StayData(models.Model):

    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        db_index = True,
        null=True,
        blank=True
    )

    stopsdata = models.ForeignKey(
        StopsData,
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

    place = models.CharField(
        null = False,
        blank = False,
        db_index = True,
        max_length = 250
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

    heads_per_room = models.IntegerField(
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

    room_type = models.CharField(
        default = "1",
        choices = cs.ROOM_TYPE,
        db_index = True,
        null = False,
        blank = False,
        max_length = 2
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

@receiver(pre_save, sender=StayData)
def staydata_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        instance.place = instance.place.lower().strip()
        instance.place_reviews = instance.place_reviews.lower().strip()
        instance.room_review = instance.room_review.lower().strip()
        instance.service_reviews = instance.service_reviews.lower().strip()


# Tolls Entry
class TollData(models.Model):

    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        db_index = True,
        null=True,
        blank=True
    )

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

@receiver(pre_save, sender=TollData)
def tolldata_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        instance.place = instance.place.lower().strip()
        instance.reviews = instance.reviews.lower().strip()
        instance.road_reviews = instance.road_reviews.lower().strip()
        instance.traffic_reviews = instance.traffic_reviews.lower().strip()


# Meals data
class MealsData(models.Model):

    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        db_index = True,
        null=True,
        blank=True
    )

    stopsdata = models.ForeignKey(
        StopsData,
        db_index = True,
        on_delete = models.SET_NULL,
        null = True
    )

    meal_type = models.CharField( 
        max_length = 1, 
        choices = cs.MEALS_CHOICES, 
        default = '1',
        db_index = True
    ) 

    gst_payable = models.BooleanField(
        db_index = True,
        default = False
    )

    service_tax_payable = models.BooleanField(
        db_index = True,
        default = False
    )

    gst_percent = models.DecimalField(
        decimal_places = 2,
        db_index = True,
        default = 0.00,
        max_digits = 2,
    )

    service_tax_percent = models.DecimalField(
        decimal_places = 2,
        db_index = True,
        default = 0.00,
        max_digits = 2,
    )

    gst_amount = models.DecimalField(
        decimal_places = 2,
        db_index = True,
        default = 0.00,
        max_digits = 10,
    )

    service_tax_amount = models.DecimalField(
        decimal_places = 2,
        db_index = True,
        default = 0.00,
        max_digits = 10,
    )

    total_amount = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        db_index = True,
        default = 0.00,
    )

    tip = models.DecimalField(
        decimal_places = 2,
        db_index = True,
        default = 0.00,
        max_digits = 10,
    )
   
    no_of_heads = models.IntegerField(
        db_index = True,
        default = 1
    )
    
    meal_reviews = models.TextField(
        null = True,
        blank = True
    )

    overall_rating = models.IntegerField(
        db_index = True,
        default = 1
    )

    preparation = models.IntegerField(
        db_index = True,
        default = 1
    )

    cleanliness = models.IntegerField(
        db_index = True,
        default = 1
    )

    service = models.IntegerField(
        db_index = True,
        default = 1
    )

    presentation = models.IntegerField(
        db_index = True,
        default = 1
    )

    hospitality = models.IntegerField(
        db_index = True,
        default = 1
    )


@receiver(pre_save, sender=TollData)
def mealsdata_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        instance.reviews = instance.reviews.lower().strip()


class MealsItem(models.Model):

    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        db_index = True,
        null=True,
        blank=True
    )

    meal = models.ForeignKey(
        MealsData,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        db_index = True
    )

    dish_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = False,
        blank = False
    )

    is_combo = models.BooleanField(
        db_index = True,
        default = False
    )

    quantity = models.DecimalField(
        decimal_places = 1,
        db_index = True,
        default = 0.0,
        max_digits = 4,
    )

    price_per_item = models.DecimalField(
        decimal_places = 2,
        db_index = True,
        default = 0.00,
        max_digits = 10,
    )

    total_amount = models.DecimalField(
        decimal_places = 2,
        db_index = True,
        default = 0.00,
        max_digits = 10,
    )

    presentation = models.IntegerField(
        db_index = True,
        default = 1
    )

    overall_rating = models.IntegerField(
        db_index = True,
        default = 1
    )

    preparation = models.IntegerField(
        db_index = True,
        default = 1
    )

    cleanliness = models.IntegerField(
        db_index = True,
        default = 1
    )

    service = models.IntegerField(
        db_index = True,
        default = 1
    )

    item_reviews = models.TextField(
        null = True,
        blank = True
    )

@receiver(pre_save, sender=TollData)
def mealsItem_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        instance.item_reviews = instance.item_reviews.lower().strip()



