import calendar
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from app.models import TourData
import random
import re

class GetCalendar:

    _calendar_output = ""
    _current_date = datetime.now()

    def __init__(self, user_id=None):
        self._user_id = user_id
        self._planned_dates = {}
        self._tourdata = self.__get_calendar_data()
        self._planned_dates_colors()


    def htmlcalendar(self):
        text_cal = calendar.HTMLCalendar(firstweekday=0)
        self._calendar_output = text_cal.formatmonth(self._current_date.year, self._current_date.month)

        self._date_highlights()
        return self._calendar_output
    

    def _generate_color_code(self):
        color_code = []
        count = 1
        while count <=3:
            hex_value = str(hex(random.randint(0,255)))

            if len(hex_value) < 2:
                count = count-1
            else:
                code = hex_value.replace("0x", "")
                print(code)
                color_code.append(code)
                count = count + 1

        return f"#D6{''.join(color_code).upper()}"


    def _planned_dates_colors(self):
        for record in self.tourdata:

            start_idx = int(record.plan_to_start_on.strftime("%d"))

            self.planned_dates.update({
                str(record.id)+"_"+str(int(record.plan_to_start_on.strftime("%d"))): {
                    "color": self.__generate_color_code(),
                    "date_range": list(range(start_idx, start_idx+record.planned_no_days+1)),
                    "tour": f"{record.source.upper()} to {record.destination.upper()}"
                }
            }) 

        print(self.planned_dates)


    def _date_highlights(self):
        soup = BeautifulSoup(self.calendar_output, features="html.parser")

        rows = soup.find_all("tr")

        html = ['<table border="0" cellpadding="0" cellspacing="0" class="month" style="margin:0px;">']

        tour_created_dates = [str(int(row.created_on.strftime("%d"))) for row in self.tourdata]

        planned_dates_key = tuple(self.planned_dates.keys())
        
        tour_started_dates = [
            str(int(row.travel_start_date.strftime("%d"))) 
            for row in self.tourdata
            if row.travel_start_date is not None
        ]

        for row in rows:
            cells = row.find_all("td")
            for cell in cells:
                if cell.text.strip() != "":
                    cell["id"] = cell.text
                    cell["style"] = "width:14%;"

                if cell.text == str(self._current_date.day):
                    cell["class"].append("current_date")

                if cell.text in tour_created_dates:
                    cell["class"].append("created_date")

                if cell.text in tour_started_dates:
                    cell["class"].append("travel_start_date")

                if cell.text in planned_dates_key:
                    cell["class"].append("planned_date")

            html.append(str(row))
        html.append("</table>")

        self.calendar_output = ''.join(html)


    def _planned_date_highlights(self):
        



    def _get_calendar_data(self):
        queryset = TourData.objects.filter(
            user_id = self.user_id,
            created_on__gte =  datetime(self.current_date.year, self.current_date.month, 1),
            created_on__lte = datetime(self.current_date.year, self.current_date.month + 1, 1) + timedelta(days=-1)
        )

        return queryset