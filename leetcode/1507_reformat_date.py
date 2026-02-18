import re

class Solution:
    def reformatDate(self, date: str) -> str:
        day, month, year = date.split()

        pattern = r'(\d+)'
        m = re.match(pattern, day)
        if m is None:
            return ""
        
        day = m.group(1)
        day = str(day).zfill(2)

        month_map = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        month = str(month_map[month]).zfill(2)

        return '-'.join([year, month, day])