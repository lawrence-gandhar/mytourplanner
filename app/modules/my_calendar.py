import calendar
from datetime import datetime
from bs4 import BeautifulSoup

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

        for row in rows:
            cells = row.find_all("td")
            for cell in cells:
                if cell.text.strip() != "":
                    cell["id"] = cell.text
                    cell["style"] = "width:14%;"

                if cell.text == str(self.current_date.day):
                    cell["class"].append("current_date")

            html.append(str(row))
        html.append("</table>")

        self.calendar_output = ''.join(html)
