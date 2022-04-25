from TouristsDestination.TouristDestinationRepo import Repo
from TouristsDestination.citiesRepo import Repo as CityRepo


class Services:
    def __init__(self, db) -> None:
        self.db = Repo(db)
        self.citydb = CityRepo(db)

    def getDestination(self, name):
        data = self.db.getDestinationByName(name)
        return data

    def getDestinationsByCity(self, cityname):
        data = self.db.getDestinationsByCity(cityname)
        description = []
        for i in data[1]:
            description.append(self.getDescription(i.blockData))
        return [data[0], data[1], description]

    def getCountOfDestinations(self):
        data = self.db.getAllDestinations()
        return len(data[1])

    def getCityByName(self, cityname):
        data = self.citydb.getCityByName(cityname)
        return data

    def addDestination(self, destination):
        verification = self.verify(destination)
        if(not verification[0]):
            return verification

        status = self.db.addTouristDestination(destination)

        if(status == False):
            return [False, "Database Error"]

        return [True, "Page Created Successfully"]

    def updateDestination(self, destination):
        verification = self.verify(destination)
        if(not verification[0]):
            return verification
        status = self.db.updateTouristDestination(destination)

        if(status == False):
            return [False, "Database Error"]

        return [True, "Page Updated Successfully"]

    def getCitiesByState(self, state):
        data = self.citydb.getCitiesByState(state)
        return data

    def getAllCities(self):
        data = self.citydb.getAllCities()
        return data

    def getAllStates(self):
        data = self.citydb.getAllCities()
        states = []
        for dict in data[1]:
            if dict['state'] not in states:
                states.append(dict['state'])
        return states

    def verify(self, destination):
        if(destination.name == ""):
            return [False, "Name Field can not remain empty"]

        if not (ord(destination.name[0]) >= 65 and ord(destination.name[0]) <= 90):
            return [False, "First letter of name should be capital"]

        if(destination.city == ""):
            return [False, "City Field can not remain empty"]

        if(destination.type == ""):
            return [False, "Type Field can not remain empty"]

        if(destination.location == ""):
            return [False, "Location Field can not remain empty"]

        if(destination.openingTime == ""):
            return [False, "Opening Time Field can not remain empty"]

        if("AM" not in destination.openingTime and "PM" not in destination.openingTime):
            return [False, "Incorrect Opening Time Format. format eg- 8:00AM"]

        if(destination.closingTime == ""):
            return [False, "Closing TIme Field can not remain empty"]

        if("AM" not in destination.closingTime and "PM" not in destination.closingTime):
            return [False, "Incorrect Closing Time Format. format eg- 6:00PM"]

        if(destination.spendingForIndian == ""):
            return [False, "spendingForIndian Field can not remain empty"]

        if(destination.spendingForForeigner == ""):
            return [False, "spendingForForeigner Field can not remain empty"]

        if("RS" not in destination.spendingForIndian):
            return [False, "Incorrect spendingForIndian Format. format eg- 100RS"]

        if("RS" not in destination.spendingForForeigner):
            return [False, "Incorrect spendingForForeigner Format.  format eg- 100RS"]

        if(destination.longitude == ""):
            return [False, "longitude Field can not remain empty"]

        isFloat = True
        try:
            float(destination.longitude)
        except:
            isFloat = False

        if(not isFloat):
            return [False, "longitude must be floating value"]

        if(destination.latitude == ""):
            return [False, "latitude Field can not remain empty"]

        isFloat = True
        try:
            float(destination.latitude)
        except:
            isFloat = False

        if(not isFloat):
            return [False, "latitude must be a floating value"]

        if(destination.timeRequired == ""):
            return [False, "timeRequired Field can not remain empty"]

        if(not destination.timeRequired.isnumeric()):
            return [False, "TIme Required must be a number"]

        if(destination.isMedCondAllowed == ""):
            return [False, "Medical Condition Field can not remain empty"]

        if(not (destination.isMedCondAllowed == "True" or destination.isMedCondAllowed == "False")):
            return [False, "Medical Condition must be either 'True' or 'False'"]

        if(not destination.rating.isnumeric() and int(destination.rating) <= 100 and int(destination.rating) >= 0):
            return [False, "Rating must between 0-100"]

        if(len(destination.blockData) < 6):
            return [False, "Atleast 6 Block Required"]

        if(len(destination.blockData) > 35):
            return [False, "Atmost 35 Block Allowed"]

        for key, value in destination.blockData.items():
            if(key == "" or value == ""):
                return [False, "Empty Block not allowed, try removing additional blocks"]

        return [True, "Verified"]

    def getDescription(self, d):
        s = d[next(iter(d))]
        count = 0
        i = 0
        while count < 2:
            if(s[i] == "."):
                count += 1
            i += 1
        return s[:i]

    def getTimeRequired(self, city):
        data = self.db.getDestinationsByCity(city)
        timeRequired = 0
        if(data[0]):
            for destination in data[1]:
                timeRequired += destination.timeRequired
            return [True, timeRequired]
        else:
            return [False, 0]
