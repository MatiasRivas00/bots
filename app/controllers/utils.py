from datetime import datetime, timedelta

def get_last_monday() -> datetime:
    today = datetime.now()
    days_since_monday = today.weekday()  # Monday is 0, Sunday is 6
    last_monday = today - timedelta(days=days_since_monday)
    # Set time to start of day
    return last_monday.replace(hour=0, minute=0, second=0, microsecond=0)