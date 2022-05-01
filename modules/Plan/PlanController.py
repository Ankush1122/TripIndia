from flask import Blueprint, render_template, redirect, request, current_app, session
from flask.helpers import url_for
import json
import pickle
import codecs
from datetime import date

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

    today = date.today()
    tempDict = json.loads(request.args.get('tempDict'))
    plandata = PlanData.PlanData("", tempDict['startingDate'], tempDict['endingDate'], tempDict['budget'], 0, tempDict['nationality'],
                                 tempDict['planType'], tempDict['noOfTravellers'], tempDict['medicalCond'], tempDict['cities'], "inactive", today.strftime("%B %d, %Y"), 0, userData[1].userid)
    skeletonPlan = planServices.generateSkeleton(plandata)

    hotels = []
    for city in plandata.cities:
        data = hotelServices.getHotelsByCity(city)
        if(data[0]):
            hotels += data[1]

    if(request.method == "POST"):
        form = request.form
        verification = planServices.verifySkeletonForm(form, len(skeletonPlan))
        if(verification[0]):
            skeletonPlan = planServices.finalSkeletonPlan(skeletonPlan, form)
            return redirect(url_for('plan.finalPlan', skeletonPlan=codecs.encode(pickle.dumps(skeletonPlan), "base64").decode(), plandata=codecs.encode(pickle.dumps(plandata), "base64").decode()))
        else:
            return render_template("skeletonPlan.html", firstname=firstname, type=userType, skeletonPlan=skeletonPlan, hotels=hotels, warning=verification[1])

    if(request.method == "GET"):
        return render_template("skeletonPlan.html", firstname=firstname, type=userType, skeletonPlan=skeletonPlan, hotels=hotels)


@ plan.route('/finalPlanPreview', methods=['GET', 'POST'])
def finalPlan():
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
        form = request.form
        planid = form.get('planid')
        print(planid)

        planServices.activatePlan(planid)
        return redirect(url_for('plan.myPlans'))

    if(request.method == "GET"):
        skeletonPlan = pickle.loads(codecs.decode(request.args.get(
            'skeletonPlan').encode(), "base64"))

        plandata = pickle.loads(codecs.decode(request.args.get(
            'plandata').encode(), "base64"))
        [planSchedule, finalCost] = planServices.generateFinalPlan(
            skeletonPlan, plandata)
        hotelCost = planServices.hotelCost(
            skeletonPlan, plandata.noOfTravellers)
        plandata.hotelCost = hotelCost
        plandata.finalCost = finalCost
        noOfRooms = (plandata.noOfTravellers + 1) // 2
        planid = planServices.generateId(plandata)
        plandata.planid = planid
        planServices.savePlan(plandata, skeletonPlan, planSchedule)
        return render_template("finalPlan.html", planid=planid, firstname=firstname, type=userType, planSchedule=planSchedule, finalCost=finalCost, hotelCost=hotelCost, noOfRooms=noOfRooms, planType=plandata.planType)


@plan.route('/myplans', methods=['GET'])
def myPlans():
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

    planDataList = planServices.getPlansByUser(userData[1].userid)
    return render_template("myPlans.html", firstname=firstname, type=userType, planDataList=planDataList)


@plan.route('/myplans/<planid>', methods=['GET'])
def planDetails(planid):
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

    [planSchedule, destinations,
        dateCreated] = planServices.getPlanByid(planid)
    return render_template('planPage.html', firstname=firstname, type=userType, planSchedule=planSchedule, destinations=destinations, dateCreated=dateCreated)


@ plan.route('/', methods=['GET'])
def redir():
    return redirect(url_for('plan.openingForm'))
