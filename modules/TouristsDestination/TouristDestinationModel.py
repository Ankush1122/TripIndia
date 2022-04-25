class TouristDestination:
    def __init__(self, index, name, state, city, type, openingTime, closingTime, spendingForIndian, spendingForForeigner, isMedCondAllowed, location, longitude, latitude, timeRequired, blockData, author, mapSrc, rating) -> None:
        self.index = index
        self.name = name
        self.state = state
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
        self.mapSrc = mapSrc
        self.rating = rating
