from django import template
from django.utils import safestring

from app.modules import custom_constants as cs
# use Library
register = template.Library()

@register.filter
def travel_mode_choice(value):
    return cs.TRAVELMODE_CHOICES_DICT[value]

@register.filter
def travel_class_choice(travel_class, travel_mode):
    return cs.TRAVELMODE_CLASS_TYPE[travel_mode][travel_class]