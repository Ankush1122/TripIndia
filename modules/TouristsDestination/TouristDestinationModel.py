class TouristDestination:
    def __init__(self, index, name, city, type, openingTime, closingTime, spendingForIndian, spendingForForeigner, isMedCondAllowed, location ,longitude, latitude, timeRequired, blockData, author) -> None:
        self.index = index
        self.name = name
        self.city = city
        self.type = type
        self.openingTime = openingTime
        self.closingTime = closingTime
        self.spendingForIndian = spendingForIndian
        self.spendingForForeigner = spendingForForeigner
        self.location = location
        self.longitude = longitude
        self.latitude = latitude
        self.timeRequired = timeRequired
        self.isMedCondAllowed = isMedCondAllowed
        self.blockData = blockData
        self.author = author
