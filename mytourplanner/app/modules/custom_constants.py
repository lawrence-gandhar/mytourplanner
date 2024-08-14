TRAVELMODE_CHOICES = (
    ('1', 'FLIGHT'),
    ('2', 'TRAIN'),
    ('3', 'BUS'),
    ('4', 'CAR'),
    ('5', 'BIKE'),
    ('6', 'CYCLE'),
    ('7', 'RENTAL/WALK'),
)

TRAVELMODE_CHOICES_DICT = {
    "1", "FLIGHT",
    "2", "TRAIN",
    "3", "BUS",
    "4", "CAR",
    "5", "BIKE",
    "6", "CYCLE",
    "7", "RENTAL/WALK",
}

TRAVELMODE_CLASS_TYPE = {
    "1": {
        "1": "Business Class",
        "2": "Economy Class",
    },
    "2": {
        "3": "AC First Class",
        "4": "AC Second Class",
        "5": "AC Third Class",
        "6": "Sleeper Coach",
        "7": "AC Seater",
        "8": "Non-AC Seater",
        "9": "General",
    },
    "3": {
        "10": "AC Sleeper Coach",
        "11": "Non-AC Sleeper Coach",
        "12": "AC Seater",
        "13": "Non-AC Seater"
    },
    "4": {
        "14": "AC Car",
        "15": "Non-AC Car"
    },
    "5": {"16": "Electric", "17": "Petrol"},
    "6": {"16": "Electric", "18": "Manual"},
    "7": {
        "19": "AC Car",
        "20": "Non-AC Car",
        "21": "Taxi",
        "22": "Autorickshaw",
        "23": "Rickshaw",
        "24": "Tram Rail",
        "25": "Metro Rail",
        "26": "Electric Bike",
        "27": "Petrol Bike",
        "28": "Electric Cycle",
        "29": "Manual Cycle"
    },
}


HALT_CHOICES = (
    ("1", "TEA/MEALS/DRINKS"),
    ("2", "WASHROOM"),
    ("3", "GAS REFILL"),
    ("4", "TOLL"),
    ("5", "STAY"),
    ("6", "BREAK"),
    ("7", "LAYOVER/CHANGE STOPS"),
    ("8", "SIGHTSEEING/LEISURE"),
    ("9", "NURSING"),
    ("9", "HOSPITAL")
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

ROOM_TYPE = (
    ("1", "SINGLE ROOM"),
    ("2", "DOUBLE ROOM"),
    ("3", "TRIPLE ROOM"),
    ("4", "DELUX DOUBLE ROOM"),
    ("5", "DELUX DOUBLE ROOM"),
    ("6", "PREMIUM DOUBLE ROOM"),
    ("7", "PREMIUM TRIPLE ROOM"),
    ("8", "HOSTEL/DOMITORY"),
    ("9", "COTTAGE"),
    ("10", "PREMIUM TRIPLE ROOM"),
    ("11", "LUXURY DOUBLE ROOM"),
    ("12", "SUITE"),
    ("13", "VILLA"),
    ("14", "TENT"),
    ("15", "HOUSEBOAT DELUXE"),
    ("16", "HOUSEBOAT PREMIUM"),
    ("18", "HOUSEBOAT LUXURY"),
    ("19", "PRESIDENTIAL SUITE"),
    ("20", "HOMESTAY"),
)

MEALS_CHOICES = (
    ("1", "TEA"),
    ("2", "BREAKFAST"),
    ("3", "BRUNCH"),
    ("4", "LUNCH"),
    ("5", "SNACKS"),
    ("6", "DINNER"),
    ("7", "DRINKS")
)