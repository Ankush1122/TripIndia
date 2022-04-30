# input data from User
class PlanData:
    def __init__(self, planid, startingDate, endingDate, travellingBudget, hotelCost, nationality, planType, noOfTravellers, isMedCond, cities, status, dateCreated, finalCost, userid) -> None:
        self.planid = planid
        self.startingDate = startingDate
        self.endingDate = endingDate
        self.travellingBudget = travellingBudget
        self.hotelCost = hotelCost
        self.nationality = nationality
        self.planType = planType
        self.noOfTravellers = noOfTravellers
        self.isMedCond = isMedCond
        self.cities = cities
        self.status = status
        self.dateCreated = dateCreated
        self.finalCost = finalCost
        self.userid = userid
