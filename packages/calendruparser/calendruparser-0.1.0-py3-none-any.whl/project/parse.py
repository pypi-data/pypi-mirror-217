import requests
from bs4 import BeautifulSoup
import datetime


class Parser:
    def __init__(self, url="https://www.calend.ru/holidays/", css_selector=".holidays .title", **kwargs):
        """
        :param url: url to parse
        :param css_selector: css selector to extract holiday names
        :param kwargs: additional parameters

        Constructor of Parser class with default parameters url and css_selector to parse holidays from calend.ru
        """
        self.url = url
        self.css_selector = css_selector

    def get_today_date(self):
        '''
        Returns today's date in format "YYYY-MM-DD"
        '''
        today = datetime.date.today()
        return today.strftime("%Y-%m-%d")

    def get_holiday(self, date):
        """

        :param date: date in format "YYYY-MM-DD"
        :return: list of holiday names or None if holiday is not found
        """
        response = requests.get(self.url + date + "/")
        soup = BeautifulSoup(response.text, 'html.parser')
        # extract holiday name from css selector
        holiday = soup.select(self.css_selector)
        # if holiday is not found, return None
        if len(holiday) == 0:
            return None
        # else return holiday names
        return [h.text.strip() for h in holiday]


if __name__ == "__main__":
    parser = Parser()
    today = parser.get_today_date()
    holiday = parser.get_holiday(today)
    print(today, holiday)
