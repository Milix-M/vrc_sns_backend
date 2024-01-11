import datetime
from zoneinfo import ZoneInfo

class Static:
    """Set the Static variables here."""

    TOKEN_CODE_EXPIRE_TIME = datetime.timedelta(minutes=15)
    ACCESS_TOKEN_EXPIRE_TIME = datetime.timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE_TIME = datetime.timedelta(days=90)
    TIME_ZONE = ZoneInfo("Asia/Tokyo")

static = Static()