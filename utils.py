import datetime

def toDateTime(qtEditDate):

    date = qtEditDate.date()
    time = qtEditDate.time()

    return datetime.datetime(date.year(), date.month(), date.day(), time.hour(), time.minute(), time.second())

def toDate(qtEditDate):

    date = qtEditDate.date()

    return datetime.date(date.year(), date.month(), date.day())

