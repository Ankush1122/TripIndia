from User import UserModel


class Repo():
    def __init__(self, db) -> None:
        self.conn = db.conn
        self.cur = db.cur

    def createUserTable(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS "User" (
                "index" SERIAL UNIQUE,
                "name" TEXT,
                "userid" TEXT PRIMARY KEY UNIQUE,
                "password" TEXT,
	            "usertype" TEXT,
	            "avatar" SMALLINT,
	            "bio" TEXT,
	            "country" TEXT,
	            "occupation" TEXT,
	            "DOB" TEXT,
                "verification" SMALLINT
            );"""
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def createUserLogsTable(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS "UserLogs" (
                "index" SERIAL UNIQUE,
                "userid" TEXT,
                "time" TEXT,
                "success" SMALLINT
            );"""
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def createUserViews(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS "Visits" (
                "index" SERIAL UNIQUE,
                "date" TEXT PRIMARY KEY UNIQUE,
                "views" INTEGER
            );"""
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def addUser(self, user):
        try:
            query = """INSERT INTO "User" ( "name" ,"userid","password","usertype","avatar","bio","country","occupation","DOB","verification") VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');""".format(
                user.name, user.userid, user.password, user.usertype, user.avatar, user.bio, user.country, user.occupation, user.DOB, user.verification)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateUserProfile(self, user):
        try:
            query = """UPDATE "User"
                    SET "name" = '{}',
                        "bio" = '{}',
                        "country" = '{}',
                        "occupation" = '{}',
                        "DOB" = '{}'
                    WHERE "userid" = '{}';""".format(user.name, user.bio, user.country, user.occupation, user.DOB, user.userid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateUserPassword(self, password, userid):
        try:
            query = """UPDATE "User"
                    SET "password" = '{}'
                    WHERE "userid" = '{}';""".format(password, userid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateUserVerificationStatus(self, userid, verification):
        try:
            query = """UPDATE "User"
                    SET "verification" = '{}'
                    WHERE "userid" = '{}';""".format(verification, userid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def isUserIdUsed(self, userid):
        try:
            query = """ SELECT * from "User" WHERE "userid" = '{}';""".format(
                userid)
            self.cur.execute(query)
            row = self.cur.fetchall()
        except Exception as e:
            print(e)
            return 1
        if(len(row)):
            return True
        else:
            return False

    def getUserById(self, userid):
        try:
            query = """ SELECT * from "User" WHERE "userid" = '{}';""".format(
                userid)
            self.cur.execute(query)
            userTable = self.cur.fetchall()
            user = UserModel.User(
                userTable[0][0], userTable[0][1], userTable[0][2], userTable[0][3], userTable[0][4], userTable[0][5], userTable[0][6], userTable[0][7], userTable[0][8], userTable[0][9], userTable[0][10])
        except Exception as e:
            print(e)
            return [False, None]
        return [True, user]

    def getUserByIndex(self, index):
        try:
            query = """ SELECT * from "User" WHERE "index" = '{}';""".format(
                index)
            self.cur.execute(query)
            userTable = self.cur.fetchall()
            user = UserModel.User(
                userTable[0][0], userTable[0][1], userTable[0][2], userTable[0][3], userTable[0][4], userTable[0][5], userTable[0][6], userTable[0][7], userTable[0][8], userTable[0][9], userTable[0][10])
        except Exception as e:
            print(e)
            return [False, None]
        return [True, user]

    def getAllUsers(self):
        try:
            query = """ SELECT * from "User"; """
            self.cur.execute(query)
            userTable = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        users = []
        for row in userTable:
            user = UserModel.User(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            users.append(user)
        return [True, users]

    def getNumberOfUsers(self):
        try:
            query = """ SELECT * from "User"; """
            self.cur.execute(query)
            userTable = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        return [True, len(userTable)]

    def deleteUserById(self, userid):
        try:
            query = """DELETE from "User" WHERE "userid" = '{}';""".format(
                userid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def deleteUserByIndex(self, index):
        try:
            query = """DELETE from "User" WHERE "index" = '{}';""".format(
                index)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def addUserLog(self, userid, time, success):
        try:
            query = """INSERT INTO "UserLogs" ( "userid", "time", "success") VALUES ('{}','{}','{}');""".format(
                userid, time, success)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def getTotalVisits(self):
        try:
            query = """ SELECT * from "Visits"; """
            self.cur.execute(query)
            VisitsTable = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        views = 0
        for row in VisitsTable:
            views += row[2]
        return [True, views]

    def getAllVisitsByDate(self):
        try:
            query = """ SELECT * from "Visits"; """
            self.cur.execute(query)
            VisitsTable = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        visits = {}
        for row in VisitsTable:
            visits[row[1]] = row[2]
        return [True, visits]

    def getVisitsByDate(self, date):
        try:
            query = """ SELECT * from "Visits" WHERE "date" = '{}'; """.format(
                date)
            self.cur.execute(query)
            VisitsTable = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        if(len(VisitsTable) == 0):
            return [False, None]
        return [True, VisitsTable[0][2]]

    def updateVisitsByDate(self, date, views):
        try:
            query = """UPDATE "Visits"
                    SET "views" = '{}'
                    WHERE "date" = '{}';""".format(views, date)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def addDateToVisitsTable(self, date):
        try:
            query = """INSERT INTO "Visits" ( "date", "views") VALUES ('{}',1);""".format(
                date)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def delteUserTable(self):
        try:
            query = """ DROP TABLE IF EXISTS "User"; """
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def deleteUserLogsTable(self):
        try:
            query = """ DROP TABLE IF EXISTS "UserLogs"; """
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def deleteVisitsTable(self):
        try:
            query = """ DROP TABLE IF EXISTS "Visits"; """
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True
