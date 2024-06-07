import calendar
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from app.models import TourData

class GetCalendar:

    calendar_output = ""
    current_date = datetime.now()

    def htmlcalendar(self):
        text_cal = calendar.HTMLCalendar(firstweekday=0)
        self.calendar_output = text_cal.formatmonth(self.current_date.year, self.current_date.month)

        self.__highlight_today()
        return self.calendar_output

    def __highlight_today(self):
        soup = BeautifulSoup(self.calendar_output, features="html.parser")

        rows = soup.find_all("tr")

        html = ['<table border="0" cellpadding="0" cellspacing="0" class="month" style="margin:0px;">']

        
        tour_created_dates = [str(int(row.created_on.strftime("%d"))) for row in self.__get_calendar_data()]
        tour_planned_dates = [
            str(int(row.plan_to_start_on.strftime("%d"))) 
            for row in self.__get_calendar_data() 
            if row.plan_to_start_on is not None
        ]
        tour_started_dates = [
            str(int(row.travel_start_date.strftime("%d"))) 
            for row in self.__get_calendar_data()
            if row.travel_start_date is not None
        ]
        
        for row in rows:
            cells = row.find_all("td")
            for cell in cells:
                if cell.text.strip() != "":
                    cell["id"] = cell.text
                    cell["style"] = "width:14%;"

                if cell.text == str(self.current_date.day):
                    cell["class"].append("current_date")

                if cell.text in tour_created_dates:
                    cell["class"].append("created_date")

                if cell.text in tour_planned_dates:
                    cell["class"].append("planned_date")

                if cell.text in tour_started_dates:
                    cell["class"].append("travel_start_date")

            html.append(str(row))
        html.append("</table>")

        self.calendar_output = ''.join(html)

    def __get_calendar_data(self):
        queryset = TourData.objects.filter(
            created_on__gte =  datetime(self.current_date.year, self.current_date.month, 1),
            created_on__lte = datetime(self.current_date.year, self.current_date.month + 1, 1) + timedelta(days=-1)
        )

        return queryset