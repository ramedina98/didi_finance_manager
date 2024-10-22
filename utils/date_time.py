# these functions helps me to handle the date and the current time
# in a more comprehensible format
from datetime import datetime

# this function helps me to obtain the current time...
def currentTime():
    time = datetime.now()

    # obtain the current hour in the following format "hh:mm:ss"
    formatted_time = time.strftime("%I-%M-%S_%p")

    return formatted_time

# this function helps me to obtain the current month and year...
def currentYearMonth():
    # this list contains all the months of the year...
    month_list = ["enero", "febrero", "marzo", "abril", "mayo",
                "junio", "julio", "agosto", "septiembre", "octubre",
                "noviembre", "diciembre"]

    # obtain the current date...
    date = datetime.today()

    # get the current month...
    month = month_list[int(date.strftime("%m").lower()) - 1]
    # get the current year...
    year = date.strftime("%Y")

    return f"{month}_{year}"