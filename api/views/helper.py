from datetime import datetime

# Helper function to add the day suffix (st, nd, rd, th)
def add_day_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return f"{day}{suffix}"

# Format the date
def format_datetime(dt):
    day = dt.day
    formatted_date = dt.strftime(f"{add_day_suffix(day)} %b %Y, %I:%M %p")
    return formatted_date
