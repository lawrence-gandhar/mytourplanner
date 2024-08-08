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
        self._planned_index = {}
        self._tourdata = self._get_calendar_data()
        self._planned_dates_colors()

    def htmlcalendar(self):
        text_cal = calendar.HTMLCalendar(firstweekday=0)
        self._calendar_output = text_cal.formatmonth(self._current_date.year, self._current_date.month)

        self._date_highlights()
        return self._calendar_output
    

    def _generate_color_code(self):
        color_code = []
        count = 1
        while count <3:
            hex_value = str(hex(random.randint(0,255))).replace("0x", "")

            if len(hex_value) < 2:
                count = count-1
            else:
                count = count + 1
                color_code.append(hex_value)
        return f"#78{''.join(color_code[:3]).upper()}"


    def _planned_dates_colors(self):
        for record in self._tourdata:

            start_idx = int(record.plan_to_start_on.strftime("%d"))

            self._planned_dates.update({
                str(record.id)+"_"+str(int(record.plan_to_start_on.strftime("%d"))): {
                    "color": self._generate_color_code(),
                    "date_range": list(range(start_idx, start_idx+record.planned_no_days+1)),
                    "tour": f"{record.source.upper()} to {record.destination.upper()}"
                }
            }) 


    def _date_highlights(self):
        soup = BeautifulSoup(self._calendar_output, features="html.parser")

        rows = soup.find_all("tr")

        html = ['<table border="0" cellpadding="0" cellspacing="0" class="month" style="margin:0px;">']

        tour_created_dates = [str(int(row.created_on.strftime("%d"))) for row in self._tourdata]

        planned_dates_key = list(x.split("_")[1] for x in list(self._planned_dates.keys()))

        tour_started_dates = [
            str(int(row.travel_start_date.strftime("%d"))) 
            for row in self._tourdata
            if row.travel_start_date is not None
        ]

        index_counter = 0
        for row in rows:
            html.append("<tr>")
            index_counter += 1
            cells = row.find_all("td")
            for cell in cells:
                index_counter += 1
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
                    self._planned_index.update({cell.text: index_counter})

                html.append(str(cell))
            html.append("</tr>")
            index_counter += 1
        html.append("</table>")
        index_counter += 1

        self._calendar_output = ''.join(html)
        self._planned_date_highlights(html)


    def _planned_date_highlights(self, html):
        soup = BeautifulSoup(self._calendar_output, features="html.parser")
        temp_html = html
        html_dict = {}
        html_enum = enumerate(html)
        for x in html_enum:
            html_dict.update({x[1]:x[0]})

        for key,val in self._planned_dates.items():

            for x in val["date_range"]:
                cell = soup.find(id=str(x))
                print(cell)
                new_tag = soup.new_tag("span", **{'class':'planned_tour'})
                new_tag.string = val["tour"]
                new_tag["style"] = f'background-color:{val["color"]};'
                cell.append(new_tag)
                # temp_html[html_dict[idx]] = str(cell)


        print(html, temp_html, html_dict)
        self._calendar_output = ''.join(temp_html)


    def _get_calendar_data(self):
        queryset = TourData.objects.filter(
            user_id = self._user_id,
            created_on__gte =  datetime(self._current_date.year, self._current_date.month, 1),
            created_on__lte = datetime(self._current_date.year, self._current_date.month + 1, 1) + timedelta(days=-1)
        )

        return queryset