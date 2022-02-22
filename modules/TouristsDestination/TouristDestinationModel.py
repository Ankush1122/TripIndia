class TouristDestination:
    def __init__(self, index, name, city, type, openingTime, closingTime, spendingForIndian, spendingForForeigner, isMedCondAllowed, locationDirection, locationDistance, timeRequired, blockData, author) -> None:
        self.index = index
        self.name = name
        self.city = city
        self.type = type
        self.openingTime = openingTime
        self.closingTime = closingTime
        self.spendingForIndian = spendingForIndian
        self.spendingForForeigner = spendingForForeigner
        self.locationDirection = locationDirection
        self.locationDistance = locationDistance
        self.timeRequired = timeRequired
        self.isMedCondAllowed = isMedCondAllowed
        self.blockData = blockData
        self.author = author
