class Event:
    def __init__(self,date,time,locationType,location,status) -> None:
        self.date = date
        self.time = time
        self.locationType = locationType
        self.location = location
        self.status = status

    def verify(self):
        pass 