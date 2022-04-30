from datetime import date


class Time():
    def getDuration(self, time1, time2):
        hours1 = self.stringToHours(time1)
        hours2 = self.stringToHours(time2)
        duration = (hours2 // 100 - hours1 // 100) * 60
        x1 = hours1 % 100
        x2 = hours2 % 100
        if(x2 >= x1):
            duration += x2 - x1
        else:
            duration -= 60 - (x1 - x2)
        return duration

    def addTimeBy(self, time, minutes):
        hours = self.stringToHours(time)
        hours += minutes // 60 * 100 + minutes % 60
        if(hours % 100 >= 60):
            rem = hours % 100
            hours = int(hours // 100 + rem // 60) * 100 + rem % 60
        hours %= 2400
        return self.hoursToString(hours)

    def stringToHours(self, time):
        hours = 0
        if(time[-2:] == "AM"):
            s = time.split(":")
            hour = int(s[0])
            if hour == 12:
                hour = 0
            hours = hour * 100 + int(s[1].split("AM")[0])
        if(time[-2:] == "PM"):
            s = time.split(":")
            hour = int(s[0])
            hours = hour * 100 + int(s[1].split("PM")[0]) + 1200
            if(hour == 12):
                hours -= 1200
        return hours

    def hoursToString(self, hours):
        if(hours >= 1200):
            hours -= 1200
            suffix = "PM"
        else:
            suffix = "AM"
        minutes = str(hours % 100)
        if len(minutes) == 1:
            minutes = "0" + minutes
        hour = str(hours // 100)
        if(hour == "0"):
            hour = "12"
        time = hour + ":" + minutes + suffix
        return time

    def pythonDate(self, day):
        year, month, day = day.split("-")
        d = date(int(year.lstrip("0")), int(
            month.lstrip("0")), int(day.lstrip("0")))
        return d
