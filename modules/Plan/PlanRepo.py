from Plan import PlanData
from Plan import PlanEvent
from Plan import SkeletonEvent
import json


class Repo:
    def __init__(self, db) -> None:
        self.conn = db.conn
        self.cur = db.cur

    def createTablePlanData(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS "PlanData" (
                "planid" TEXT UNIQUE PRIMARY KEY,
                "startingDate" TEXT,
                "endingDate" TEXT,
                "travellingBudget" INTEGER,
                "hotelCost" INTEGER,
                "nationality" TEXT,
                "planType" TEXT,
	            "noOfTravellers" SMALLINT,
                "isMedCond" TEXT,
                "cities" TEXT,
                "status" TEXT,
                "dateCreated" TEXT,
                "finalCost" INTEGER,
                "userid" TEXT,
                "index" SERIAL
            );"""
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def CreateTableSkeletonPlan(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS "SkeletonPlan" (
                "planid" TEXT,
                "date" TEXT,
                "city" TEXT,
                "startingTime" TEXT,
                "endingTime" TEXT,
                "stayingHotel" TEXT,
                "index" INTEGER
            );"""
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def CreateTablePlanSchedule(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS "PlanSchedule" (
                "planid" TEXT,
                "date" TEXT,
                "startingTime" TEXT,
                "endingTime" TEXT,
                "destination" TEXT,
                "city" TEXT,
                "index" INTEGER
            );"""
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def addPlanData(self, plandata):
        try:
            query = """INSERT INTO "PlanData" ( "planid","startingDate","endingDate","travellingBudget","hotelCost","nationality","planType","noOfTravellers","isMedCond","cities","status","dateCreated","finalCost","userid") VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');""".format(
                plandata.planid, plandata.startingDate, plandata.endingDate, plandata.travellingBudget, plandata.hotelCost, plandata.nationality, plandata.planType, plandata.noOfTravellers, plandata.isMedCond, json.dumps(plandata.cities), plandata.status, plandata.dateCreated, plandata.finalCost, plandata.userid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def addSkeletonPlan(self, skeletonPlan, index):
        try:
            query = """INSERT INTO "SkeletonPlan" ( "planid","date","city","startingTime","endingTime","stayingHotel","index") VALUES ('{}','{}','{}','{}','{}','{}','{}');""".format(
                skeletonPlan.planid, skeletonPlan.date, skeletonPlan.city, skeletonPlan.startingTime, skeletonPlan.endingTime, skeletonPlan.stayingHotel, index)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def addPlanSchedule(self, planSchedule, index):
        try:
            query = """INSERT INTO "PlanSchedule" ( "planid","date","startingTime","endingTime","destination","city","index") VALUES ('{}','{}','{}','{}','{}','{}','{}');""".format(
                planSchedule.planid, planSchedule.date, planSchedule.startingTime, planSchedule.endingTime, planSchedule.destination, planSchedule.city, index)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def getPlanDataByid(self, planid):
        try:
            query = """ SELECT * from "PlanData" WHERE "planid" = '{}';""".format(
                planid)
            self.cur.execute(query)
            data = self.cur.fetchall()
            plandata = PlanData.PlanData(
                data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], data[0][8], json.loads(data[0][9]), data[0][10], data[0][11], data[0][12], data[0][13])
        except Exception as e:
            print(e)
            return [False, None]
        return [True, plandata]

    def getSkeletonPlanByid(self, planid):
        try:
            query = """ SELECT * from "SkeletonPlan" WHERE "planid" = '{}' ORDER BY "index" ASC;""".format(
                planid)
            self.cur.execute(query)
            Table = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        skeletonPlan = []
        for data in Table:
            skeletonEvent = SkeletonEvent.SkeletonEvent(
                data[0], data[1], data[2], data[3], data[4], data[5])
            skeletonPlan.append(skeletonEvent)
        return [True, skeletonPlan]

    def getPlanScheduleByid(self, planid):
        try:
            query = """ SELECT * from "PlanSchedule" WHERE "planid" = '{}' ORDER BY "index" ASC;""".format(
                planid)
            self.cur.execute(query)
            Table = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        PlanSchedule = []
        for data in Table:
            planEvent = PlanEvent.Event(
                data[0], data[1], data[2], data[3], data[4], data[5])
            PlanSchedule.append(planEvent)
        return [True, PlanSchedule]

    def activatePlanData(self, planid, status):
        try:
            query = """UPDATE "PlanData"
                    SET "status" = '{}'
                    WHERE "planid" = '{}';""".format(status, planid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def getPlanDataByUserid(self, userid):
        try:
            query = """ SELECT * from "PlanData" WHERE "userid" = '{}' ORDER  BY "index" DESC ;""".format(
                userid)
            self.cur.execute(query)
            table = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]

        planDataList = []
        for data in table:
            plandata = PlanData.PlanData(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], json.loads(data[9]), data[10], data[11], data[12], data[13])
            if(plandata.status == "active"):
                planDataList.append(plandata)
        return [True, planDataList]

    def getAllPlanData(self):
        try:
            query = """ SELECT * from "PlanData" WHERE "status" = 'active';""".format()
            self.cur.execute(query)
            table = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]

        planDataList = []
        for data in table:
            plandata = PlanData.PlanData(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], json.loads(data[9]), data[10], data[11], data[12], data[13])
            if(plandata.status == "active"):
                planDataList.append(plandata)
        return [True, planDataList]

    def deletePlanDataByid(self, planid):
        try:
            query = """DELETE from "PlanData" WHERE "planid" = '{}';""".format(
                planid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def deleteSkeletonPlanByid(self, planid):
        try:
            query = """DELETE from "SkeletonPlan" WHERE "planid" = '{}';""".format(
                planid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def deletePlanScheduleByid(self, planid):
        try:
            query = """DELETE from "PlanSchedule" WHERE "planid" = '{}';""".format(
                planid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def deleteTablePlanData(self):
        try:
            query = """ DROP TABLE IF EXISTS "PlanData"; """
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def deleteTableSkeletonPlan(self):
        try:
            query = """ DROP TABLE IF EXISTS "SkeletonPlan"; """
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def deleteTablePlanSchedule(self):
        try:
            query = """ DROP TABLE IF EXISTS "PlanSchedule"; """
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True
