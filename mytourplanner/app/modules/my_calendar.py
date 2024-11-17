import calendar
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import random
import re

from app.modules import tourdata_db_operations as tourdata_dbops
from app.modules import custom_constants as cs

from django.utils.safestring import mark_safe

class GetCalendar:
    
    def __init__(self):

        self._calendar_output = ""
        self.current_date = None
        self._user_id = None
        self.queryset = None
        self._planned_dates = {}
        self._planned_index = {}
        self._selected_colors = []
        self._travel_start = {}
        self._travel_mode_data = {}
        self.current_date = datetime.now()
        self.today = datetime.now().day
        self.today_month = datetime.now().month
        self.today_year = datetime.now().year
        
    #============================================================
    # Create & Return HtmlCalender with all details
    #============================================================
    def htmlcalendar(self, user_id=None, queryset=None, month=None, year=None):

        self._user_id = user_id
        self.queryset = queryset

        if all([month, year]):
            self.current_date = datetime(year, month, 1)

        self._tourdata = self._get_calendar_data()
        self._planned_dates_formatter()
        text_cal = calendar.HTMLCalendar(firstweekday=0)
        self._calendar_output = text_cal.formatmonth(self.current_date.year, self.current_date.month)
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

        while True:
            color = random.choice(color_code)
            if color not in self._selected_colors and color is not None:
                self._selected_colors.append(color)
                return color.upper()
            
    #============================================================
    # Generate Dictionary for Planned Dates Formatting
    #============================================================
    def _planned_dates_formatter(self):
        for record in self._tourdata:
            if record["plan_to_start_on"] is not None:
                start_idx = int(record["plan_to_start_on"].strftime("%d"))
            
            if record["travel_start_date"]:
                start_idx = int(record["travel_start_date"].strftime("%d"))

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
                travel_mode_date = int(record["tour_data__travel_date"].strftime("%d"))
                travel_details = f"""
                    Travelling from {record["tour_data__source"]} to {record["tour_data__destination"]}. 
                    By {cs.TRAVELMODE_CHOICES_DICT[record["tour_data__travel_mode"]]}. 
                """

                if travel_mode_date not in self._travel_mode_data:
                    self._travel_mode_data.update({travel_mode_date: {
                        "travel_details":travel_details, 
                        "color": self._planned_dates[str(start_idx)]["color"]
                    }})
                else:
                    self._travel_mode_data[travel_mode_date]["travel_details"] = travel_details
                    self._travel_mode_data[travel_mode_date]["color"] = self._planned_dates[str(start_idx)]["color"]

    #============================================================
    # Fetch Queryset
    #============================================================
    def _get_calendar_data(self):

        created_on_gte = datetime(self.current_date.year, self.current_date.month, 1)

        if self.current_date.month < 12:
            created_on_lte = datetime(self.current_date.year, self.current_date.month + 1, 1) + timedelta(days=-1)
        else:
            created_on_lte = datetime(self.current_date.year + 1, 1, 1) + timedelta(days=-1)

        return tourdata_dbops.fetch_calendar_data(queryset=self.queryset, start_date=created_on_gte, end_date=created_on_lte)
    
    #============================================================
    # Put all details in the Calendar
    #============================================================
    def _complete_soup(self):
        soup = BeautifulSoup(self._calendar_output, features="html.parser")
        rows = soup.find_all("tr")

        #
        # create prev/next month buttons in <th>
        #
        icon_bg = """
            position:relative; 
            display:inline; 
            width:20px; 
            height:20px;
            background-color: #000000;
            border-radius: 100%;
            padding: 5px;
            cursor: pointer;
            color: #fff;
        """

        month_holder = soup.find("th", class_="month")
        prev_btn = soup.new_tag("span", **{"year":self.current_date.year, "month":self.current_date.month - 1})
        prev_btn["style"] = icon_bg+"float:left;"
        prev_btn["id"] = "month-prev-btn"

        prev_icon = soup.new_tag("i", **{"class": "fas fa-chevron-left"})
        prev_btn.append(prev_icon)

        next_btn = soup.new_tag("span", **{"year":self.current_date.year, "month":self.current_date.month + 1})
        next_btn["style"] = icon_bg + "float:right;"
        next_btn["id"] = "month-next-btn"

        next_icon = soup.new_tag("i", **{"class": "fas fa-chevron-right"})
        next_btn.append(next_icon)

        month_holder.append(prev_btn) 
        month_holder.append(next_btn)

        today_month_year = datetime.strptime(month_holder.text.strip(), "%B %Y").strftime("%m-%Y").split("-")

        is_today = False
        if (self.today_month == int(today_month_year[0]) and self.today_year == int(today_month_year[1])):
            is_today = True
        

        #
        # style the columns 
        #
        for row in rows:
            cells = row.find_all("td")
            for cell in cells:
                if cell.text.strip() != "":
                    cell["id"] = cell.text
                    cell["style"] = "width:14%;text-align:center;padding:5px 0px 5px 0px;"

                if cell.text == str(self.today) and is_today:
                    cell["class"].append("current_date")

        #
        # substitute data and style the columns based on the data
        #       
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

        #
        for key, value in self._travel_mode_data.items():
            cell = soup.find(id=key)
            new_tag = soup.new_tag("span", **{'class':'planned_tour', 'title':value["travel_details"]})
            new_tag["style"] = f"background-color:{value["color"]};"
            new_tag.string = mark_safe(value["travel_details"])
            cell.append(new_tag)


        self._calendar_output = soup.prettify()