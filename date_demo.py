"""
Demo CLI
"""
import sys
import argparse
from datetime import date

months = [
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december"
]

thirty_one_days = ["january", "march", "may", "july", "august", "october", "december"]
thirty_days = ["april", "june", "september", "november"]

def real_month(month):
    """
    If the month name is passed in convert it to the integer value and if the month
    was passed in as an integer validate it is a valid number (1-12)
    """
    try:
        int_month = int(month)
    except ValueError:
        if month.lower() in months:
            int_month = months.index(month.lower()) + 1
    if int_month not in range(1, 13):
        raise argparse.ArgumentTypeError("{} is not a valid month".format(month))

    return int_month


def validate_day(day, month):
    """
    validate the number day actually exists in the specified month
    """
    if months[month-1] in thirty_one_days:
        assert 1 <= day <= 31
    if months[month-1] in thirty_days:
        assert 1 <= day <= 30
    if months[month-1] == "february":
        assert 1 <= day <= 29

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # create the parser and add arguments
    parser = argparse.ArgumentParser(
        prog='date_demo.py',
        description="Get the day of the week from any date"
    )
    parser.add_argument(
        'day',
        help="Enter a valid day of the month (1-31)",
        type=int,
        choices=range(1, 32),
        metavar='day'
    )
    parser.add_argument(
        'month',
        help="Enter a month as a number (1-12) or the full name of the month as a string",
        type=real_month
    )
    parser.add_argument(
        'year',
        help="Enter a year as 4 digits",
        type=int
    )

    opts = parser.parse_args(argv)

    # validate the month day combo here since we can't compare the two
    # until after we parse the args
    try:
        validate_day(opts.day, opts.month)
    except AssertionError:
        parser.error("Invalid month/day combination!")

    try:
        my_date = date(opts.year, opts.month, opts.day)
    except ValueError:
        if opts.day == 29 and opts.month == 2:
            print("{} wasn't a leap year!".format(opts.year))
            return
        else:
            raise

    today = date.today()

    # print the date and day of the week in relation to what today is
    if my_date == today:
        print("{} is today! Today is {}".format(
            my_date.strftime('%d %B, %Y'), my_date.strftime('%A')))
    if my_date < today:
        print("{} was a {}".format(
            my_date.strftime('%d %B, %Y'), my_date.strftime('%A')))
    if my_date > today:
        print("{} will be a {}".format(
            my_date.strftime('%d %B, %Y'), my_date.strftime('%A')))

if __name__ == '__main__':
    main()
