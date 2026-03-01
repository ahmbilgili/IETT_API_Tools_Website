from datetime import tzinfo, timedelta

class TurkishTimezone(tzinfo):
    def tzname(self, dt):
        return super().tzname(dt)
    
    def dst(self, dt):
        return super().dst(dt)

    def utcoffset(self, dt):
        # UTC + 3 (GMT+3)
        return timedelta(hours=3)