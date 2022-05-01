from datetime import date, datetime, timedelta
import time
from operator import attrgetter

from TouristsDestination import TouristDestinationServices
from Plan import SkeletonEvent
from Plan import PlanEvent
from Plan import Time
from Plan import PlanRepo
from Hotel import HotelServices


class Services:
    def __init__(self, db) -> None:
        self.touristDestinationServices = TouristDestinationServices.Services(
            db)
        self.hotelServices = HotelServices.Services(db)
        self.planRepo = PlanRepo.Repo(db)

    def verifyOpeningForm(self, startingDate, endingDate, budget, noOfCities):
        time = Time.Time()

        if(startingDate == "" or endingDate == ""):
            return [False, "Please Fill Tour Dates"]

        if(startingDate > endingDate):
            return [False, "Invalid Tour Dates"]

        if(int(budget / 500) < noOfCities):
            return [False, "Please Increase Budget Or Reduce Number Of Cities"]

        d0 = time.pythonDate(startingDate)

        d1 = time.pythonDate(endingDate)

        duration = (d1 - d0).days + 1

        today = date.today()
        if(d1 < today):
            return [False, "Invalid Tour Dates, Tour Ending Date already Passed"]

        if(duration > 365):
            return [False, "Plan Duration Should Not Exceed 1 Year"]

        if(noOfCities > duration):
            return [False, str(noOfCities) + " Cities Can't Be Travelled In " + str(duration) + " Days"]

        return ["True", ""]

    def getNoOfPlans(self):
        data = self.planRepo.getAllPlanData()
        if data[0]:
            return len(data[1])
        else:
            return 0

    def verifyCitiesForm(self, Cities):
        unique = []
        for city in Cities:
            if(city not in unique):
                unique.append(city)
            else:
                return [False, "All Cities Must Be Unique"]
        return [True, ""]

    def generateSkeleton(self, planData):
        time = Time.Time()
        d0 = time.pythonDate(planData.startingDate)

        d1 = time.pythonDate(planData.endingDate)

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
            event = SkeletonEvent.SkeletonEvent("tempid", time.pythonDate(
                planData.startingDate) + timedelta(days=j), planData.cities[i], "10:00AM", "5:00PM", "")
            skeletonPlan.append(event)
            if(cityFreq[planData.cities[i]] <= 0):
                i += 1

        return skeletonPlan

    def verifySkeletonForm(self, form, len):
        time = Time.Time()
        for i in range(1, len + 1):
            if(time.stringToHours(form.get('startingTime' + str(i))) > time.stringToHours(form.get('endingTime' + str(i)))):
                return [False, "Invalid Travelling Time On " + form.get('date' + str(i))]
        return [True, None]

    def finalSkeletonPlan(self, skeletonPlan, form):
        i = 1
        for event in skeletonPlan:
            event.startingTime = form.get('startingTime' + str(i))
            event.endingTime = form.get('endingTime' + str(i))
            event.stayingHotel = form.get('hotel' + str(i))
            i += 1
        return skeletonPlan

    def generateFinalPlan(self, skeletonPlan, plandata):
        time = Time.Time()
        visitedDestination = []
        planSchedule = []
        budgetRem = int(plandata.travellingBudget)
        for event in skeletonPlan:
            currentTime = event.startingTime
            endingTime = event.endingTime
            destinations = self.touristDestinationServices.getDestinationsByCity(
                event.city)[1]

            if(plandata.planType == "Most Popular"):
                destinations.sort(key=attrgetter('rating'),
                                  reverse=True)

            elif(plandata.planType == "Budget Efficient"):
                # sorting destinationa by budget/timeRequired
                for destination in destinations:
                    if(plandata.nationality == "Indian"):
                        spending = destination.spendingForIndian.split("RS")[0]
                    else:
                        spending = destination.spendingForForeigner.split("RS")[
                            0]
                    destination.index = int(
                        spending) / int(destination.timeRequired)
                destinations.sort(key=attrgetter('index'))

            elif(plandata.planType == "Time Efficient"):
                destinations.sort(key=attrgetter('timeRequired'))

            for destination in destinations:
                duration = time.getDuration(currentTime, endingTime)
                budget = 0
                if(plandata.nationality == "Indian"):
                    budget = int(destination.spendingForIndian[:-2])
                else:
                    budget = int(destination.spendingForForeigner[:-2])

                if(int(destination.timeRequired) <= duration and budget <= budgetRem and destination.name not in visitedDestination and not (not plandata.isMedCond and destination.isMedCondAllowed == "False")):
                    budgetRem -= budget
                    newTime = time.addTimeBy(
                        currentTime, int(destination.timeRequired))
                    planevent = PlanEvent.Event(
                        "", event.date, currentTime, newTime, destination.name, destination.city)
                    visitedDestination.append(destination.name)
                    planSchedule.append(planevent)
                    currentTime = newTime
        return [planSchedule, int(plandata.travellingBudget) - budgetRem]

    def hotelCost(self, skeletonPlan, noOfTourists):
        noOfRooms = (noOfTourists + 1) // 2
        cost = 0
        prevCost = 0
        prevHotel = ""
        for event in skeletonPlan:
            if(event.stayingHotel != prevHotel):
                data = self.hotelServices.getHotel(event.stayingHotel)
                prevHotel = data[1].name
                prevCost = data[1].roomPrice
            cost += prevCost * noOfRooms
        return cost

    def savePlan(self, plandata, skeletonPlan, planSchedule):
        self.planRepo.addPlanData(plandata)

        planid = plandata.planid
        i = 0
        for event in skeletonPlan:
            event.planid = planid
            self.planRepo.addSkeletonPlan(event, i)
            i += 1
        i = 0
        for event in planSchedule:
            event.planid = planid
            self.planRepo.addPlanSchedule(event, i)
            i += 1

    def generateId(self, plandata):
        id = plandata.userid + plandata.dateCreated + str(time.time())
        return id

    def activatePlan(self, planid):
        self.planRepo.activatePlanData(planid, "active")

    def getPlansByUser(self, userid):
        time = Time.Time()
        data = self.planRepo.getPlanDataByUserid(userid)
        if data[0]:
            for plan in data[1]:
                today = date.today()
                d1 = time.pythonDate(today.strftime("%y-%m-%d"))
                d2 = time.pythonDate(plan.endingDate)
                if(d1 > d2):
                    plan.status = "expired"
            return data[1]

    def getPlanByid(self, planid):
        data = self.planRepo.getPlanScheduleByid(planid)
        planData = self.planRepo.getPlanDataByid(planid)
        destinations = {}
        timeNow = datetime.now()
        for event in data[1]:
            destinationData = self.touristDestinationServices.getDestination(
                event.destination)

            if(planData[1].nationality == "Indian"):
                destinationCost = destinationData[1].spendingForIndian
            else:
                destinationCost = destinationData[1].spendingForForeigner

            destinations[destinationData[1].name] = [
                destinationData[1].type, destinationData[1].rating, destinationCost]

            timeStart = datetime.strptime(
                event.date + ' ' + event.startingTime, '%Y-%m-%d %I:%M%p')

            timeEnd = datetime.strptime(
                event.date + ' ' + event.endingTime, '%Y-%m-%d %I:%M%p')
            if(timeStart > timeNow):
                event.status = "Pending"
            elif(timeEnd < timeNow):
                event.status = "Expired"
            else:
                event.status = "Current"

        return [data[1], destinations, planData[1].dateCreated]
