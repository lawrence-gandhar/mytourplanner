import calendar
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import random
import re

from app.modules import db_operations as dbops
from app.modules import custom_constants as cs

from django.utils.safestring import mark_safe

class GetCalendar:

    _calendar_output = ""
    _current_date = datetime.now()

    def __init__(self, user_id=None, queryset=None):
        self._user_id = user_id
        self.queryset = queryset
        self._planned_dates = {}
        self._planned_index = {}
        self._selected_colors = []
        self._travel_start = {}
        self._tourdata = self._get_calendar_data()
        self._planned_dates_formatter()
        

    #============================================================
    # Create & Return HtmlCalender with all details
    #============================================================
    def htmlcalendar(self):
        text_cal = calendar.HTMLCalendar(firstweekday=0)
        self._calendar_output = text_cal.formatmonth(self._current_date.year, self._current_date.month)
        self._complete_soup()
        return self._calendar_output
    
    #============================================================
    # Generate Color Codes for planned dates
    #============================================================
    def _generate_color_code(self):
        color_code = (
            "#003cb3", "#003399", "#002b80", # blue shades
            "#008000", "#006600", "#004d00", "#336600", "#264d00", # Green shades
            "#990099", "#d752ff", "#660066", # purple shades
            "#b30059", "#99004d", "#800040", # pink shades
            "#cc0052", "#b30047", "#99003d", # crimson shades
            "#990000", "#800000", # red shades
            "#009999", "#008080", "#006666" # teal shades
        )

        color = random.choice(color_code)
        if color is not None:
            if color not in self._selected_colors:
                self._selected_colors.append(color)
                return color.upper()
            else:
                self._generate_color_code()
        else:
            self._generate_color_code()

    #============================================================
    # Generate Dictionary for Planned Dates Formatting
    #============================================================
    def _planned_dates_formatter(self):
        for record in self._tourdata:

            start_idx = int(record["plan_to_start_on"].strftime("%d"))

            date_range = [start_idx]
            if record["planned_no_days"] > 1:
                date_range = list(range(start_idx, (start_idx + record["planned_no_days"])))    

            self._planned_dates.update({
                str(start_idx): {
                    "color": self._generate_color_code(),
                    "date_range": date_range,
                    "tour": f"{record["source"].upper()} to {record["destination"].upper()}",
                    "data": record,
                    "planned_date": record["plan_to_start_on"]
                }
            }) 

            travel_mode_found = False
            if record["travel_start_date"]:
                travel_start = int(record["travel_start_date"].strftime("%d"))
                if record["tour_data__travel_mode"]:
                    travel_mode = f"""{cs.TRAVELMODE_CHOICES_DICT[record["tour_data__travel_mode"]]} from
                        {record["travel_source"].upper()} to {record["travel_destination"].upper()}""" 
                    travel_mode_found = True

                self._travel_start.update({
                    str(travel_start): {
                        "planned_date": str(start_idx),
                        "travel_mode": travel_mode,
                        "travel_mode_found": travel_mode_found
                    }
                })

            if travel_mode_found:
                

    #============================================================
    # Fetch Queryset
    #============================================================
    def _get_calendar_data(self):

        created_on_gte = datetime(self._current_date.year, self._current_date.month, 1)
        created_on_lte = datetime(self._current_date.year, self._current_date.month + 1, 1) + timedelta(days=-1)

        return dbops.fetch_calendar_data(queryset=self.queryset, start_date=created_on_gte, end_date=created_on_lte)
    
    #============================================================
    # Put all details in the Calendar
    #============================================================
    def _complete_soup(self):
        soup = BeautifulSoup(self._calendar_output, features="html.parser")
        rows = soup.find_all("tr")

        tour_started_dates = [
            str(int(row["travel_start_date"].strftime("%d"))) 
            for row in self._tourdata
            if row["travel_start_date"] is not None
        ]

        for row in rows:
            cells = row.find_all("td")
            for cell in cells:
                if cell.text.strip() != "":
                    cell["id"] = cell.text
                    cell["style"] = "width:14%;text-align:center;padding:5px 0px 5px 0px;"

                if cell.text == str(self._current_date.day):
                    cell["class"].append("current_date")

                if cell.text in tour_started_dates:
                    background_color = self._planned_dates[self._travel_start[cell.text]["planned_date"]]["color"]
                    cell["style"] = f"""background-color:{background_color}; color:#ffffff; font-weight:bold; 
                                        text-align:center;padding:5px 0px 5px 0px;"""
                    
        for val in self._planned_dates.values():
            for tour in val["date_range"]:
                cell = soup.find(id=str(tour))
                new_tag = soup.new_tag("span", **{'class':'planned_tour', 'title':f"Planned Tour - {val["tour"].upper()}"})
                new_tag["style"] = f"background-color:{val["color"]}"
                new_tag.string = val["tour"].upper()
                cell.append(new_tag)

        for travel_key, travel_value in self._travel_start.items():
            if not travel_value["travel_mode_found"]:
                tour = self._planned_dates[travel_value["planned_date"]]["tour"]
                color = self._planned_dates[travel_value["planned_date"]]["color"]
                planned_date = self._planned_dates[travel_value["planned_date"]]["planned_date"].strftime("%d %B, %Y")

                cell = soup.find(id=travel_key)
                new_tag = soup.new_tag("span", **{'class':'planned_tour', 'title':tour})
                new_tag["style"] = f"background-color:{color};"
                new_tag.string = mark_safe(f"Travelling From {tour} as planned. Date: {planned_date}")
                cell.append(new_tag)

            if travel_value["travel_mode_found"]:
                title = f"Travelling by {travel_value["travel_mode"]}"
                cell = soup.find(id=travel_key)
                new_tag = soup.new_tag("span", **{'class':'planned_tour', 'title':title})
                new_tag["style"] = f"background-color:{self._planned_dates[travel_value["planned_date"]]["color"]}"
                new_tag.string = f"Travelling by {travel_value["travel_mode"]}"
                cell.append(new_tag)

        self._calendar_output = soup.prettify()