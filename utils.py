import datetime

# converts a 4-byte BUP date to a Python datetime
# ported from bup_getdate()
def convert_bytes_to_Datetime(date_id):

    # minutes
    mins = (date_id % 60) & 0xFF

    hours = int(date_id % (60*24) / 60) & 0xFF

    # Compute days count
    div = date_id / (60*24);
    div = int(div)

    year_base   = int(div / ((365*4) + 1))
    year_base = int(year_base * 4)
    days_remain = int(div % ((365*4) + 1))

    days_count = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    month = 0;

    for i in range(0, 48):
        days_per_month = days_count[i % 12];
        if i == 1:
            days_per_month += 1

        if days_remain < days_per_month:
            break

        days_remain -= days_per_month
        month += 1

        if i % 12 == 11:
            month = 0
            year_base += 1

    year_base += 1980
    month += 1
    days_remain += 1

    return datetime.datetime(year_base, month, days_remain, hours, mins)

# returns the language based on the langId
def get_language(langId):

    if langId == 0:
        return "Japanese"
    elif langId == 1:
        return "English"
    elif langId == 2:
        return "Francais"
    elif langId == 3:
        return "Deutsch"
    elif langId == 4:
        return "Espanol"
    elif langId == 5:
        return "Italiano"

    # language not found
    return None