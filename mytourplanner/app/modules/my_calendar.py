import calendar
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from app.models import TourData
import random
import re

class GetCalendar:

    _calendar_output = ""
    _current_date = datetime.now()

    def __init__(self, user_id=None, queryset=None):
        self._user_id = user_id
        self.queryset = queryset
        self._planned_dates = {}
        self._planned_index = {}
        self._selected_colors = []
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
            "#990099", "#800080", "#660066", # purple shades
            "#b30059", "#99004d", "#800040", # pink shades
            "#cc0052", "#b30047", "#99003d", # crimson shades
            "#990000", "#800000", # red shades
            "#009999", "#008080", "#006666" # teal shades
        )

        color = random.choice(color_code)

        if color not in self._selected_colors:
            self._selected_colors.append(color)
            return color.upper()
        else:
            self._generate_color_code()

    #============================================================
    # Generate Dictionary for Planned Dates Formatting
    #============================================================
    def _planned_dates_formatter(self):
        for record in self._tourdata:

            start_idx = int(record["plan_to_start_on"].strftime("%d"))

            self._planned_dates.update({
                str(int(record["plan_to_start_on"].strftime("%d"))): {
                    "color": self._generate_color_code(),
                    "date_range": list(range(start_idx, start_idx+record["planned_no_days"]+1)),
                    "tour": f"{record["source"].upper()} to {record["destination"].upper()}"
                }
            }) 

    #============================================================
    # Fetch Queryset
    #============================================================
    def _get_calendar_data(self):

        created_on_gte = datetime(self._current_date.year, self._current_date.month, 1)
        created_on_lte = datetime(self._current_date.year, self._current_date.month + 1, 1) + timedelta(days=-1)

        queryset = self.queryset.filter(
            created_on__gte =  created_on_gte,
            created_on__lte = created_on_lte
        ).values(
            'id', 'created_on', 'plan_to_start_on', 'travel_start_date', 'travel_end_date', 
            'source', 'destination', 'planned_no_days'
        )

        return queryset
    
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
                    cell["class"].append("travel_start_date")

        for key, val in self._planned_dates.items():
            for tour in val["date_range"]:
                cell = soup.find(id=str(tour))
                new_tag = soup.new_tag("span", **{'class':'planned_tour'})
                new_tag["style"] = f"background-color:{val["color"]}"
                new_tag.string = val["tour"].upper()
                cell.append(new_tag)
        self._calendar_output = soup.prettify()