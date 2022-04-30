from Hotel import HotelModel


class Repo:
    def __init__(self, db) -> None:
        self.conn = db.conn
        self.cur = db.cur

    def createTable(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS "Hotel" (
                "name" TEXT UNIQUE PRIMARY KEY,
                "city" TEXT,
	            "hotelType" SMALLINT,
                "roomCapacity" SMALLINT,
                "roomPrice" INTEGER,
                "longitude" TEXT,
                "latitude" TEXT
            );"""
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def addHotel(self, hotel):
        try:
            query = """INSERT INTO "Hotel" ( "name","city","hotelType","roomCapacity","roomPrice","longitude","latitude") VALUES ('{}','{}','{}','{}','{}','{}','{}');""".format(
                hotel.name, hotel.city, hotel.hotelType, hotel.roomCapacity, hotel.roomPrice, hotel.longitude, hotel.latitude)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def getHotelByName(self, name):
        try:
            query = """ SELECT * from "Hotel" WHERE "name" = '{}';""".format(
                name)
            self.cur.execute(query)
            data = self.cur.fetchall()
            hotel = HotelModel.Model(
                data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6])
        except Exception as e:
            print(e)
            return [False, None]
        return [True, hotel]

    def getAllHotels(self):
        try:
            query = """ SELECT * from "Hotel"; """
            self.cur.execute(query)
            table = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        hotels = []
        for data in table:
            hotel = HotelModel.Model(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            hotels.append(hotel)
        return [True, hotels]

    def getHotelsByCity(self, cityname):
        try:
            query = """ SELECT * from "Hotel"
                        WHERE "city" = '{}'; """.format(cityname)
            self.cur.execute(query)
            table = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        hotels = []
        for data in table:
            hotel = HotelModel.Model(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            hotels.append(hotel)
        return [True, hotels]

    def deleteHotelByName(self, name):
        try:
            query = """DELETE from "Hotel" WHERE "name" = '{}';""".format(
                name)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def deleteHotelTable(self):
        try:
            query = """ DROP TABLE IF EXISTS "Hotel"; """
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True
