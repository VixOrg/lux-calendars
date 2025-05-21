import os
from datetime import date, timedelta
from icalendar import Calendar, Event

def calculate_easter(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return date(year, month, day)

fixed_holidays = [
    {"month": 1, "day": 1, "summary": "New Year's Day"},
    {"month": 5, "day": 1, "summary": "Labour Day"},
    {"month": 5, "day": 9, "summary": "Europe Day"},
    {"month": 6, "day": 23, "summary": "National Day"},
    {"month": 8, "day": 15, "summary": "Assumption Day"},
    {"month": 11, "day": 1, "summary": "All Saints' Day"},
    {"month": 12, "day": 25, "summary": "Christmas Day"},
    {"month": 12, "day": 26, "summary": "Boxing Day"},
]

calendar_path = "public-holidays.ics"

# Start with a clean calendar
cal = Calendar()
cal.add("prodid", "-//Luxembourg Public Holidays//EN")
cal.add("version", "2.0")

years_in_future = int(os.getenv("YEARS_IN_FUTURE", 10))
years_in_past = int(os.getenv("YEARS_IN_PAST", 1))
current_year = date.today().year

for year in range(current_year - years_in_past, current_year + years_in_future + 1): # the end of the range is excluded in range function
    # Add fixed holidays
    for holiday in fixed_holidays:
        event_date = date(year, holiday["month"], holiday["day"])
        event = Event()
        event.add("dtstart", event_date)
        event.add("summary", holiday["summary"])
        cal.add_component(event)

    # Add sliding holidays
    easter = calculate_easter(year)
    sliding_holidays = [
        {"date": easter, "summary": "Easter"},
        {"date": easter + timedelta(days=1), "summary": "Easter Monday"},
        {"date": easter + timedelta(days=39), "summary": "Ascension Day"},
        {"date": easter + timedelta(days=50), "summary": "Whit Monday"},
    ]
    for holiday in sliding_holidays:
        event = Event()
        event.add("dtstart", holiday["date"])
        event.add("summary", holiday["summary"])
        cal.add_component(event)

# Save updated calendar
with open(calendar_path, "wb") as f:
    f.write(cal.to_ical())
