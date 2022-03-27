from crypt import methods
from flask import Blueprint, render_template, redirect, request, current_app, session
from flask.helpers import url_for
import os
from flask_mail import Message

touristdestination = Blueprint("touristdestination", __name__, static_folder="static",
                               template_folder="templates")


from TouristsDestination.TouristDestinationServices import Services
from TouristsDestination.TouristDestinationModel import TouristDestination
from User import UserServices
from app import db, mail


@touristdestination.route('/explore', methods=['GET'])
def explore():
    if (not session.get("index") is None):
        userService = UserServices.UserServices(db)
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]
            usertype = userData[1].usertype
    else:
        userData = [False]
        firstname = ""
        usertype = ""
    service = Services(db)
    cities = service.getAllCities()
    return render_template("citiesList.html", loggedIn=userData[0], firstname=firstname, cities=cities[1], type=usertype)


@touristdestination.route('/explore/<cityname>', methods=['GET'])
def places(cityname):
    if (not session.get("index") is None):
        userService = UserServices.UserServices(db)
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]
            usertype = userData[1].usertype
    else:
        userData = [False]
        firstname = ""
        usertype = ""
    service = Services(db)
    data = service.getDestinationsByCity(cityname)
    cityData = service.getCityByName(cityname)
    if(data[0] and cityData[0]):
        return render_template("placesList.html", loggedIn=userData[0], firstname=firstname, destinations=data[1], cityname=cityname, type=usertype, descriptions=data[2])
    else:
        return redirect(url_for('touristdestination.explore'))


@touristdestination.route('/explore/<cityname>/<destination>', methods=['GET'])
def touristDestination(cityname, destination):
    userService = UserServices.UserServices(db)
    if (not session.get("index") is None):
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]
            userid = userData[1].userid
            usertype = userData[1].usertype
    else:
        userData = [False, None]
        firstname = ""
        userid = ""
        usertype = ""
    service = Services(db)
    data = service.getDestination(destination)
    if(data[0] and data[1].city == cityname):
        data[1].timeRequired = int((data[1].timeRequired + 30) / 60)
        authorname = userService.getUserName(data[1].author)

        return render_template('placeinfo.html', loggedIn=userData[0], firstname=firstname, destination=data[1], authorname=authorname, userid=userid, type=usertype)
    else:
        print("redirecting")
        return redirect(url_for('touristdestination.explore'))


@touristdestination.route('/addDestination/<place>', methods=['GET', 'POST'])
def addDestination(place):
    if (not session.get("index") is None):
        userService = UserServices.UserServices(db)
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

    newPlace = (place == "new")
    service = Services(db)
    states = service.getAllStates()
    cities = service.getAllCities()

    if(request.method == "POST"):

        formdata = request.form
        blockData = {}
        for i in range(1, 100):
            title = "title" + str(i)
            data = "data" + str(i)
            if title in formdata:
                blockData[formdata.get(title)] = formdata.get(data)
        destination = TouristDestination(None, formdata.get(
            "name"), formdata.get("state"), formdata.get("city"), formdata.get("type"), formdata.get("openingTime"), formdata.get("closingTime"), formdata.get("spendingForIndian"), formdata.get("spendingForForeigner"), formdata.get("isMedCondAllowed"), formdata.get("location"), formdata.get("longitude"), formdata.get("latitude"), formdata.get("timeRequired"), blockData, userData[1].userid)

        if(newPlace):
            data = service.addDestination(destination)
            if(data[0]):
                return redirect(url_for('touristdestination.upload', destinationname=destination.name))
        else:
            data = service.updateDestination(destination)
            if(data[0]):
                return render_template('addDestination.html', success=data[1], firstname=firstname, loggedIn=userData[0], destination=destination, count=len(destination.blockData), statesList=states, citiesList=cities[1])
        return render_template('addDestination.html', warning=data[1], firstname=firstname, loggedIn=userData[0], destination=destination, count=len(destination.blockData), statesList=states, citiesList=cities[1])

    if(request.method == "GET"):
        if(newPlace):
            destination = TouristDestination(
                "", "", "", "", "", "", "", "", "", "", "", "", "", "", None, "")
            return render_template('addDestination.html', loggedIn=userData[0], firstname=firstname, destination=destination, count=5, statesList=states, citiesList=cities[1])
        else:
            data = service.getDestination(place)
            if(data[0] and data[1].author == userData[1].userid):
                return render_template('addDestination.html', loggedIn=userData[0], firstname=firstname, destination=data[1], count=len(data[1].blockData), statesList=states, citiesList=cities[1])
            else:
                return "You are not authorised to access this page"


@touristdestination.route('/uploadimages/<destinationname>', methods=['GET', 'POST'])
def upload(destinationname):
    if (not session.get("index") is None):
        userService = UserServices.UserServices(db)
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
            return redirect(url_for("touristdestination.sendImages", destination=destinationname))
        else:
            return render_template('uploadImages.html', warning="Database Error")

    if(request.method == "GET"):
        return render_template('uploadImages.html', loggedIn=userData[0], firstname=firstname)


@touristdestination.route('/sendImages/<destination>')
def sendImages(destination):
    mes = Message("TripIndia Uploaded Images", recipients=[
                  current_app.config.get("ADMIN_ADDRESS")])

    with current_app.open_resource(current_app.config.get("IMAGE_UPLOADS") + destination + "0.jpg") as img0:
        mes.attach(destination + "0.jpg", 'image/jpg', img0.read())

    with current_app.open_resource(current_app.config.get("IMAGE_UPLOADS") + destination + "1.jpg") as img1:
        mes.attach(destination + "1.jpg", 'image/jpg', img1.read())

    with current_app.open_resource(current_app.config.get("IMAGE_UPLOADS") + destination + "2.jpg") as img2:
        mes.attach(destination + "2.jpg", 'image/jpg', img2.read())

    with current_app.open_resource(current_app.config.get("IMAGE_UPLOADS") + destination + "3.jpg") as img3:
        mes.attach(destination + "3.jpg", 'image/jpg', img3.read())

    mail.send(mes)
    return redirect(url_for('touristdestination.explore'))


@touristdestination.route('/', methods=['GET'])
def redir():
    return redirect(url_for('touristdestination.explore'))
