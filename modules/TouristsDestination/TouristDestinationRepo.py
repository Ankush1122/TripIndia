from TouristsDestination import TouristDestinationModel
import MainRepo
import json


class Repo(MainRepo.Repo):
    def createTouristDestinationTable(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS "TouristDestination" (
                "index" SERIAL UNIQUE,
                "name" TEXT UNIQUE PRIMARY KEY,
                "city" TEXT,
	            "type" TEXT,
                "openingtime" TEXT,
                "closingtime" TEXT,
                "spendingforindian" TEXT,
                "spendingforforeigner" TEXT,
                "isMedCondAllowed" TEXT,
                "locationdirection" TEXT,
                "locationdistance" TEXT,
                "timerequired" INTEGER,
                "blockData" TEXT,
                "author" TEXT
            );"""
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def addTouristDestination(self, destination):
        try:
            query = """INSERT INTO "TouristDestination" ( "name" ,"city","type","openingtime","closingtime","spendingforindian","spendingforforeigner","isMedCondAllowed","locationdirection","locationdistance","timerequired","blockData","author") VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');""".format(
                destination.name, destination.city, destination.type, destination.openingTime, destination.closingTime, destination.spendingForIndian, destination.spendingForForeigner, destination.isMedCondAllowed, destination.locationDirection, destination.locationDistance, destination.timeRequired, json.dumps(destination.blockData), destination.author)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def getDestinationByName(self, name):
        try:
            query = """ SELECT * from "TouristDestination" WHERE "name" = '{}';""".format(
                name)
            self.cur.execute(query)
            data = self.cur.fetchall()
            destination = TouristDestinationModel.TouristDestination(
                data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], data[0][8], data[0][9], data[0][10], data[0][11], json.loads(data[0][12]), data[0][13])
        except Exception as e:
            print(e)
            return [False, None]
        return [True, destination]

    def getDestinationByIndex(self, index):
        try:
            query = """ SELECT * from "TouristDestination" WHERE "index" = '{}';""".format(
                index)
            self.cur.execute(query)
            data = self.cur.fetchall()
            destination = TouristDestinationModel.TouristDestination(
                data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], data[0][8], data[0][9], data[0][10], data[0][11], json.loads(data[0][12]), data[0][13])
        except Exception as e:
            print(e)
            return [False, None]
        return [True, destination]

    def getAllDestinations(self):
        try:
            query = """ SELECT * from "TouristDestination"; """
            self.cur.execute(query)
            table = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        destinations = []
        for data in table:
            destination = TouristDestinationModel.TouristDestination(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], json.loads(data[12]), data[13])
            destinations.append(destination)
        return [True, destinations]

    def getDestinationsByCity(self, cityname):
        try:
            query = """ SELECT * from "TouristDestination"
                        WHERE "city" = '{}'; """.format(cityname)
            self.cur.execute(query)
            table = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        destinations = []
        for data in table:
            destination = TouristDestinationModel.TouristDestination(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], json.loads(data[12]), data[13])
            destinations.append(destination)
        return [True, destinations]

    def deleteDestinationByName(self, name):
        try:
            query = """DELETE from "TouristDestination" WHERE "name" = '{}';""".format(
                name)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def deleteDestinationByIndex(self, index):
        try:
            query = """DELETE from "TouristDestination" WHERE "index" = '{}';""".format(
                index)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def delteTouristDestinationTable(self):
        try:
            query = """ DROP TABLE IF EXISTS "TouristDestination"; """
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True
