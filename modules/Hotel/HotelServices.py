from Hotel import HotelRepo


class Services:
    def __init__(self, db) -> None:
        self.db = HotelRepo.Repo(db)

    def addHotel(self, hotel):
        data = self.db.addHotel(hotel)
        if(data):
            return [data, "Hotel Added Succesfully"]
        else:
            return [data, "Database Error"]

    def getHotelsByCity(self, city):
        data = self.db.getHotelsByCity(city)
        return data

    def getHotel(self, name):
        data = self.db.getHotelByName(name)
        return data
