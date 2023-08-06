__all__ = [
        'YEAR_RAW',
        'MONTH_RAW',
        'DAY_RAW',
        'MONTH_YEAR_RAW',
        'DAY_MONTH_YEAR_RAW',
        'DateTimeLocalRegex'
]

import datetime
import re

from dtmodel.base._types import Regex
from dtmodel.functions import *

AGE_RAW = r"(?P<age>\d{1,3}[.,]\d+|\d{1,3})"
YEAR_RAW = r'(?P<year>(19|20)\d\d)'
MONTH_RAW = r'(?P<month>10|11|12|[0]?[1-9])'
DAY_RAW = r'(?P<day>3[0-1]|[1-2][0-9]|[0]?[1-9])'
MONTH_YEAR_RAW = r'{}[.\-/]{}'.format(MONTH_RAW, YEAR_RAW)
DAY_MONTH_YEAR_RAW = r'{}[.\-/]{}[.\-/]{}'.format(DAY_RAW, MONTH_RAW, YEAR_RAW)


class DateTimeLocalRegex(Regex):
    def __init__(self, value: str, start: datetime.date =None):
        self.value = value
        self.start = start
        self._age = None
        self.date = None
        if self.value is None:
            self.date = datetime.date.today()
        else:
            day_month_year = re.search(DAY_MONTH_YEAR_RAW, self.value)
            if day_month_year:
                self._year = day_month_year.group('year')
                self._month = day_month_year.group('month')
                self._day = day_month_year.group('day')
                self.date = datetime.date(int(self._year), int(self._month), int(self._day))
            else:
                month_year = re.search(MONTH_YEAR_RAW, self.value)
                if month_year:
                    self._year = day_month_year.group('year')
                    self._month = day_month_year.group('month')
                    self._day = '1'
                    self.date = datetime.date(int(self._year), int(self._month), int(self._day))
                else:
                    year = re.search(YEAR_RAW, self.value)
                    if year:
                        self._year = day_month_year.group('year')
                        self._month = '7'
                        self._day = '1'
                        self.date = datetime.date(int(self._year), int(self._month), int(self._day))
                    else:
                        age = re.search(AGE_RAW, self.value)
                        if age:
                            digits = age.groupdict()['age']
                            self._age = digits.replace(',', '.')
                            if self.start:
                                self.date = self.start + datetime.timedelta(days=int(self._age)*365)
        if self.date:
            super().__init__(str(self.date))
        else:
            super().__init__(self.value)
            
    @property
    def age(self):
        if self._age:
            return float(self._age)
        elif self.date:
            if self.start:
                return years(self.start, self.date)
        return None
        
