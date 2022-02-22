from flask import Blueprint, render_template, redirect, request, current_app, session
from flask.helpers import url_for
from TouristsDestination.TouristDestinationServices import Services
from TouristsDestination.TouristDestinationModel import TouristDestination
from User import UserServices
import os

touristdestination = Blueprint("touristdestination", __name__, static_folder="static",
                               template_folder="templates")


@touristdestination.route('/explore/rajasthan', methods=['GET'])
def exploreRajasthan():
    if (not session.get("index") is None):
        userService = UserServices.UserServices(current_app.config)
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]
    else:
        userData = [False]
        firstname = ""
    return render_template("rajasthan.html", loggedIn=userData[0], firstname=firstname)


@touristdestination.route('/explore/rajasthan/<cityname>', methods=['GET'])
def places(cityname):
    if (not session.get("index") is None):
        userService = UserServices.UserServices(current_app.config)
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]
    else:
        userData = [False]
        firstname = ""
    service = Services(current_app.config)
    data = service.getDestinationsByCity(cityname)
    cityData = service.getCityByName(cityname)
    if(data[0] and cityData[0]):
        return render_template("places.html", loggedIn=userData[0], firstname=firstname, destinations=data[1], city=cityData[1])
    else:
        return redirect(url_for('touristdestination.exploreRajasthan'))


@touristdestination.route('/explore/rajasthan/<cityname>/<destination>', methods=['GET'])
def touristDestination(cityname, destination):
    userService = UserServices.UserServices(current_app.config)
    if (not session.get("index") is None):
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]
    else:
        userData = [False, None]
        firstname = ""
    service = Services(current_app.config)
    data = service.getDestination(destination)
    if(data[0] and data[1].city == cityname):
        dir = ""
        for i in range(len(data[1].locationDirection)):
            if(data[1].locationDirection[i] == "N"):
                dir += "North"
            if(data[1].locationDirection[i] == "S"):
                dir += "South"
            if(data[1].locationDirection[i] == "E"):
                dir += "East"
            if(data[1].locationDirection[i] == "W"):
                dir += "West"
            if i == 0:
                dir += "-"
        location = data[1].locationDistance + \
            "km " + dir + " of " + data[1].city + " city"
        data[1].timeRequired = int((data[1].timeRequired + 30) / 60)
        authorname = userService.getUserName(data[1].author)
        return render_template('touristdestination.html', loggedIn=userData[0], firstname=firstname, destination=data[1], location=location, authorname=authorname)
    else:
        print("redirecting")
        return redirect(url_for('touristdestination.exploreRajasthan'))


@touristdestination.route('/addDestination', methods=['GET', 'POST'])
def addDestination():
    if (not session.get("index") is None):
        userService = UserServices.UserServices(current_app.config)
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]
    else:
        userData = [False]
        firstname = ""

    if(userData[0] == False or not (userData[1].usertype == "admin" or userData[1].usertype == "superadmin")):
        return redirect(url_for('user.login'))

    if(request.method == "POST"):

        formdata = request.form
        blockData = {}
        for i in range(1, 31):
            title = "title" + str(i)
            data = "data" + str(i)
            if title in formdata:
                blockData[formdata.get(title)] = formdata.get(data)
        destination = TouristDestination(None, formdata.get(
            "name"), formdata.get("city"), formdata.get("type"), formdata.get("openingTime"), formdata.get("closingTime"), formdata.get("spendingForIndian"), formdata.get("spendingForForeigner"), formdata.get("isMedCondAllowed"), formdata.get("locationDirection"), formdata.get("locationDistance"), formdata.get("timeRequired"), blockData, userData[1].userid)

        service = Services(current_app.config)
        data = service.addDestination(destination)
        if(data[0]):
            return redirect(url_for('touristdestination.upload', destinationname=destination.name))

        else:
            return render_template('addDestination.html', warning=data[1], firstname=firstname, loggedIn=userData[0])

    if(request.method == "GET"):
        return render_template('addDestination.html', loggedIn=userData[0], firstname=firstname)


@touristdestination.route('/uploadimages/<destinationname>', methods=['GET', 'POST'])
def upload(destinationname):
    if (not session.get("index") is None):
        userService = UserServices.UserServices(current_app.config)
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]
    else:
        userData = [False]
        firstname = ""

    if(userData[0] == False or not (userData[1].usertype == "admin" or userData[1].usertype == "superadmin")):
        return redirect(url_for('user.login'))

    if(request.method == "POST"):
        if(request.files):
            files = request.files.getlist("images[]")
            count = 0
            if(len(files) != 4):
                return render_template('uploadImages.html', warning="Four Images must be Uploaded")

            for file in files:
                file.save(os.path.join(
                    current_app.config['IMAGE_UPLOADS'], destinationname + str(count) + ".jpg"))
                count += 1
            return redirect(url_for("sendImages", destination=destinationname))
        else:
            return render_template('uploadImages.html', warning="Database Error")

    if(request.method == "GET"):
        return render_template('uploadImages.html', loggedIn=userData[0], firstname=firstname)


@touristdestination.route('/', methods=['GET'])
def redir():
    return redirect(url_for('touristdestination.exploreRajasthan'))