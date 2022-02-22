#!/usr/bin/python

import database
import Event

class Plan:
    events = []
    def __init__(self) -> None:
        pass

    def generatePlan(self,bugdet,timeOfStay,medicalCond,generationMethod):
        if  (generationMethod == "ByPopularity"):
            self.generateByPopularity(bugdet,timeOfStay,medicalCond)
        elif(generationMethod == "ByMaxPlaces"):
            self.generateByMaxPlaces(bugdet,timeOfStay,medicalCond)

    def generateByPopularity(self,budget,timeOfStay,medicalCond):
        db = database()
        touristSpots = db.readTouristDestinations()

    def generateByMaxPlaces(self,budget,timeOfStay,medicalCond):
        pass