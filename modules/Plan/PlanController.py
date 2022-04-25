from flask import Blueprint, render_template, redirect, request, current_app, session
from flask.helpers import url_for
import json

plan = Blueprint("plan", __name__, static_folder="static",
                 template_folder="templates")


from User import UserServices
from Plan import PlanData
from Plan import PlanServices
from Hotel import HotelServices
from app import db

userService = UserServices.UserServices(db)
planServices = PlanServices.Services(db)
hotelServices = HotelServices.Services(db)


@plan.route('/openingForm', methods=['GET', 'POST'])
def openingForm():
    if (not session.get("index") is None):
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            userType = userData[1].usertype
            firstname = name
            if " " in name:
                firstname = name.split()[0]
    else:
        userData = [False]
        userType = ""
        firstname = ""

    if(userData[0] == False):
        return redirect(url_for('user.login'))

    if(request.method == "POST"):
        openingForm = request.form

        if(openingForm.get('medicalCond') == "Yes"):
            medicalCond = True
        else:
            medicalCond = False

        data = planServices.verifyOpeningForm(openingForm.get(
            'startingDate'), openingForm.get('endingDate'), int(openingForm.get('budget')), int(openingForm.get('noOfCities')))
        if(data[0]):
            tempDict = {"startingDate": openingForm.get(
                'startingDate'), "endingDate": openingForm.get('endingDate'), "budget": openingForm.get('budget'), "nationality": openingForm.get('nationality'), "planType": openingForm.get('planType'), "noOfTravellers": int(openingForm.get('noOfTravellers')), "medicalCond": medicalCond}
            return redirect(url_for('plan.citiesForm', noOfCities=openingForm.get('noOfCities'), tempDict=json.dumps(tempDict)))
        else:
            return render_template("openingForm.html", startingDate=openingForm.get(
                'startingDate'), endingDate=openingForm.get('endingDate'), firstname=firstname, type=userType, warning=data[1])

    elif(request.method == "GET"):
        state = request.args.get('state')
        startingDate = request.args.get('startingDate')
        endingDate = request.args.get('endingDate')
        return render_template("openingForm.html", startingDate=startingDate, endingDate=endingDate, firstname=firstname, type=userType)


@plan.route('/citiesForm', methods=['GET', 'POST'])
def citiesForm():
    if (not session.get("index") is None):
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            userType = userData[1].usertype
            firstname = name
            if " " in name:
                firstname = name.split()[0]
    else:
        userData = [False]
        userType = ""
        firstname = ""

    if(userData[0] == False):
        return redirect(url_for('user.login'))

    noOfCities = int(request.args.get('noOfCities'))
    tempDict = json.loads(request.args.get('tempDict'))

    if(request.method == "POST"):
        citiesForm = request.form
        cities = []
        for i in range(1, noOfCities + 1):
            cities.append(citiesForm.get('city' + str(i)))
        data = planServices.verifyCitiesForm(cities)
        if(data[0]):
            tempDict['cities'] = cities
            return redirect(url_for('plan.skeletonPlan', tempDict=json.dumps(tempDict)))
        else:
            return render_template("citiesForm.html", noOfCities=noOfCities, firstname=firstname, type=userType, warning=data[1])

    elif(request.method == "GET"):
        return render_template("citiesForm.html", noOfCities=noOfCities, firstname=firstname, type=userType)


@plan.route('/skeletonPlan', methods=['GET', 'POST'])
def skeletonPlan():
    if (not session.get("index") is None):
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            userType = userData[1].usertype
            firstname = name
            if " " in name:
                firstname = name.split()[0]
    else:
        userData = [False]
        userType = ""
        firstname = ""

    if(userData[0] == False):
        return redirect(url_for('user.login'))

    tempDict = json.loads(request.args.get('tempDict'))
    plandata = PlanData.PlanData(tempDict['startingDate'], tempDict['endingDate'], tempDict['budget'], tempDict['nationality'],
                                 tempDict['planType'], tempDict['noOfTravellers'], tempDict['medicalCond'], tempDict['cities'])
    skeletonPlan = planServices.generateSkeleton(plandata)

    if(request.method == "POST"):
        return "This Module Is Under Development"

    if(request.method == "GET"):
        hotels = []
        for city in plandata.cities:
            data = hotelServices.getHotelsByCity(city)
            if(data[0]):
                hotels += data[1]
        return render_template("skeletonPlan.html", firstname=firstname, type=userType, skeletonPlan=skeletonPlan, hotels=hotels)


@plan.route('/', methods=['GET'])
def redir():
    return redirect(url_for('plan.generate'))
