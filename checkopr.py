import re
import csv
import datetime
import calendar
from dateutil import parser
from var_dump import var_dump


class OpeningHoursFormatException(Exception):
    def __init__(self):
        Exception.__init__(self, "Error opening hours format in file, pls check!")


class Restaurant(object):
    WEEKDAYS = list(calendar.day_abbr)
    WEEKDAYS_RE = '|'.join(map(str, WEEKDAYS))

    def __init__(self, name, hours):
        self.name = name
        self.daily_hours = [None] * 7
        self.parse_hours(hours)

    def di(self, day):
        return self.WEEKDAYS.index(day)

    def parse_hours(self, hours):
        hs = hours.split("/")

        def parse_dt(hours_string):
            for wd in self.WEEKDAYS:
                hours_string = hours_string.replace(wd, '')
            return hours_string.replace('-', '').replace('"', '')

        for h in hs:
            try:
                odt = parser.parse(parse_dt(h.split(' - ')[0]))
                cdt = parser.parse(parse_dt(h.split(' - ')[1]))
            except ValueError:
                raise OpeningHoursFormatException()

            o = (odt.hour, odt.minute)
            c = (cdt.hour, cdt.minute)

            days = re.search(
                r"((?P<sd>({0}))\-(?P<ed>({0}))(\,\s(?P<xd>({0})))?|(?P<od>({0})))".format(self.WEEKDAYS_RE),
                h
            ).groupdict()

            if days['sd']:
                for i in range(self.di(days['sd']), self.di(days['ed']) + 1):
                    self.daily_hours[i] = (o, c)
                if days['xd']:
                    self.daily_hours[self.di(days['xd'])] = (o, c)
            elif days['od']:
                self.daily_hours[self.di(days['od'])] = (o, c)

    def is_open(self, dt):
        d = dt.weekday()
        if self.daily_hours[d]:
            o, c = self.daily_hours[d]
            odt = datetime.datetime(dt.year, dt.month, dt.day, o[0], o[1])
            cdt = datetime.datetime(dt.year, dt.month, dt.day, c[0], c[1])

            return True if odt <= dt <= cdt else False
        else:
            return False


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def find_open_restaurants(csv_filename, d='Sun', t='19:30'):
    today = datetime.datetime.today()

    h, m = map(int, t.split(':'))
    idx = list(calendar.day_abbr).index(d)
    d = next_weekday(today, idx).day

    goal_datetime = datetime.datetime(today.year, today.month, d, h, m)

    rl = []
    with open(csv_filename, 'r') as f:
        r = csv.reader(f)
        for row in r:
            restaurant_obj = Restaurant(*row)
            if restaurant_obj.is_open(goal_datetime):
                rl.append(restaurant_obj.name)

    return rl


if __name__ == '__main__':

    hour = 1
    minute = 40
    goal_day = 'Mon'
    goal_time = '{}:{}'.format(hour, minute)

    var_dump(find_open_restaurants("restaurant_hours.csv", goal_day, goal_time))
