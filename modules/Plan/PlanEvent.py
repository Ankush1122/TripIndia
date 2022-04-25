# Storing - At particular time - location(place) where tourist is supposed to visit

class Event:
    def __init__(self, planid, date, startingTime, endingTime, destinationType, destination) -> None:
        self.planid = planid
        self.date = date
        self.startingTime = startingTime
        self.endingTime = endingTime
        self.destination = destination
        self.destinationType = destinationType
