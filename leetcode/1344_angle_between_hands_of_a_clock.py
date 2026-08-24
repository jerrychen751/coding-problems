class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        '''
        60 minutes -> 360 degrees; 1 min is 6 degrees
        hour hand degrees = (hour / 12) * 360
        min hand degrees = (min / 60) * 360
        smaller angle between them -> abs(min_deg - hr_deg) % 180
        '''
        min_frac = minutes / 60
        min_deg = min_frac * 360
        hr_frac = (hour % 12) / 12
        hr_deg = (hr_frac * 360) + (min_frac * 30)
        diff = abs(hr_deg - min_deg)
        return min(diff, 360 - diff)
