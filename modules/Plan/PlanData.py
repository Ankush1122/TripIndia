# input data from User
class PlanData:
    def __init__(self, startingDate, endingDate, budget, nationality, planType, noOfTravellers, isMedCond, cities) -> None:
        self.status = "active"
        self.startingDate = startingDate
        self.endingDate = endingDate
        self.budget = budget
        self.nationality = nationality
        self.planType = planType
        self.noOfTravellers = noOfTravellers
        self.isMedCond = isMedCond
        self.cities = cities
