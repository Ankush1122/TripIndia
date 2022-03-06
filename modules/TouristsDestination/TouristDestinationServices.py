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
        return data

    def getCityByName(self, cityname):
        data = self.citydb.getCityByName(cityname)
        return data

    def addDestination(self, destination):
        if(destination.name == ""):
            return [False, "Name Field can not remain empty"]

        if not (ord(destination.name[0]) >= 65 and ord(destination.name[0]) <= 90):
            return [False, "First letter of name should be capital"]

        if(destination.city == ""):
            return [False, "City Field can not remain empty"]

        if(destination.type == ""):
            return [False, "Type Field can not remain empty"]

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

        if(destination.locationDirection == ""):
            return [False, "locationDirection Field can not remain empty"]

        dir = ["N", "S", "E", "W", "NW", "NE", "SW", "SE"]

        if(destination.locationDirection not in dir):
            return [False, "Incorrect locationDirection format. It should be one of N/S/E/W/NE/NW/SE/SW"]

        if(destination.locationDistance == ""):
            return [False, "locationDistance Field can not remain empty"]

        if(not destination.locationDistance.isnumeric()):
            return [False, "locationDistance must be a number"]

        if(destination.timeRequired == ""):
            return [False, "timeRequired Field can not remain empty"]

        if(not destination.timeRequired.isnumeric()):
            return [False, "TIme Required must be a number"]

        if(destination.isMedCondAllowed == ""):
            return [False, "isMedCondAllowed Field can not remain empty"]

        if(not (destination.isMedCondAllowed == "True" or destination.isMedCondAllowed == "False")):
            return [False, "isMedCondAllowed must be 'True' or 'False'"]

        if(len(destination.blockData) < 5):
            return [False, "Atleast 5 Block Required"]

        if(len(destination.blockData) > 30):
            return [False, "Atmost 30 Block Allowed"]

        for key, value in destination.blockData.items():
            if(key == "" or value == ""):
                return [False, "Empty Block not allowed, try removing additional blocks"]

        status = self.db.addTouristDestination(destination)

        if(status == False):
            return [False, "Database Error"]

        return [True, "Page Created Successfully By "]

    def getCitiesByState(self, state):
        data = self.citydb.getCitiesByState(state)
        return data
