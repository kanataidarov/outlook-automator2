def to_dt_str(ews_dt, tz):
    """Formats EWSDateTime object as datetime string.
    """
    return ews_dt.astimezone(tz).strftime('%Y-%m-%d %H:%M')
