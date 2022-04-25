# Basic Sekeleton of Plan - Storing - At Particular Date - City where Tourist is supposed to be
# And storing travelling period(starting and ending time of travel) on that day

class SkeletonEvent:
    def __init__(self, planid, date, city, startingTime, endingTime, stayingHotel) -> None:
        self.planid = planid
        self.date = date
        self.city = city
        self.startingTime = startingTime
        self.endingTime = endingTime
        self.stayingHotel = stayingHotel
