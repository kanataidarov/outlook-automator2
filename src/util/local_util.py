import pytz


def to_dt_str(ews_dt):
    """Formats EWSDateTime object as datetime string.
    """
    return ews_dt.astimezone(pytz.timezone("Asia/Aqtobe")).strftime('%Y-%m-%d %H:%M')
