from datetime import date, timedelta
from TouristsDestination import TouristDestinationServices
from Plan import SkeletonEvent


class Services:
    def __init__(self, db) -> None:
        self.touristDestinationServices = TouristDestinationServices.Services(
            db)

    def verifyOpeningForm(self, startingDate, endingDate, budget, noOfCities):
        if(startingDate == "" or endingDate == ""):
            return [False, "Please Fill Tour Dates"]

        if(startingDate > endingDate):
            return [False, "Invalid Tour Dates"]

        if(int(budget / 500) < noOfCities):
            return [False, "Please Increase Budget Or Reduce Number Of Cities"]

        d0 = self.pythonDate(startingDate)

        d1 = self.pythonDate(endingDate)

        duration = (d1 - d0).days + 1

        today = date.today()
        if(d1 < today):
            return [False, "Invalid Tour Dates, Tour Ending Date already Passed"]

        if(duration > 365):
            return [False, "Plan Duration Should Not Exceed 1 Year"]

        if(noOfCities > duration):
            return [False, str(noOfCities) + " Cities Can't Be Travelled In " + str(duration) + " Days"]

        return ["True", ""]

    def verifyCitiesForm(self, Cities):
        unique = []
        for city in Cities:
            if(city not in unique):
                unique.append(city)
            else:
                return [False, "All Cities Must Be Unique"]
        return [True, ""]

    def generateSkeleton(self, planData):

        d0 = self.pythonDate(planData.startingDate)

        d1 = self.pythonDate(planData.endingDate)

        duration = (d1 - d0).days + 1

        timeRequired = {}
        for city in planData.cities:
            data = self.touristDestinationServices.getTimeRequired(city)
            if(data[0]):
                timeRequired[city] = data[1]
            else:
                return [False, "Database Error"]

        sortedCityList = list(dict(
            sorted(timeRequired.items(), key=lambda item: item[1], reverse=True)).keys())
        cityFreq = {}

        i = 0
        for j in range(duration):
            if(j == i):
                cityFreq[sortedCityList[i]] = 1
            else:
                cityFreq[sortedCityList[i]] += 1

            i += 1
            if(i >= len(planData.cities)):
                i = 0

        skeletonPlan = []
        i = 0
        for j in range(duration):
            cityFreq[planData.cities[i]] -= 1
            event = SkeletonEvent.SkeletonEvent("tempid", self.pythonDate(
                planData.startingDate) + timedelta(days=j), planData.cities[i], "10:00AM", "5:00PM", "")
            skeletonPlan.append(event)
            if(cityFreq[planData.cities[i]] <= 0):
                i += 1

        return skeletonPlan

    def pythonDate(self, day):
        year, month, day = day.split("-")
        d = date(int(year.lstrip("0")), int(
            month.lstrip("0")), int(day.lstrip("0")))
        return d
