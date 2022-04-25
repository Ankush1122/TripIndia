from crypt import methods
import MainRepo
from flask import Flask, render_template, redirect, session, send_file, request
from flask_mail import Mail, Message
from flask.helpers import url_for

import os

app = Flask(__name__)


if(os.environ.get('ENV') == "Production"):
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

mail = Mail(app)
db = MainRepo.Repo(app.config)

from User import UserServices
from TouristsDestination import TouristDestinationServices
from User.UserController import user
from Plan.PlanController import plan
from Hotel.HotelController import hotel
from TouristsDestination.TouristDestinationController import touristdestination

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(touristdestination, url_prefix="/touristdestination")
app.register_blueprint(plan, url_prefix="/plan")
app.register_blueprint(hotel, url_prefix="/hotel")


@app.route('/home', methods=['GET'])
def home():
    userService = UserServices.UserServices(db)
    touristServices = TouristDestinationServices.Services(db)

    if(app.config["ENV"] == "production"):
        userService.addView()
    totalVisits = userService.getTotalVisits()
    plans = 0
    noOfusers = userService.getNumberOfUsers()
    places = touristServices.getCountOfDestinations()
    if (not session.get("index") is None):
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]
            return render_template("home1.html", firstname=firstname, loggedIn=True, type=userData[1].usertype, visits=totalVisits, plans=plans, noOfusers=noOfusers, places=places, warning="")

    return render_template('home1.html', loggedIn=False, visits=totalVisits, plans=plans, noOfusers=noOfusers, places=places)


@app.route('/planData', methods=['POST', 'GET'])
def planData():
    if(request.method == "POST"):
        userService = UserServices.UserServices(db)
        touristServices = TouristDestinationServices.Services(db)

        if(app.config["ENV"] == "production"):
            userService.addView()
        totalVisits = userService.getTotalVisits()
        plans = 0
        noOfusers = userService.getNumberOfUsers()
        places = touristServices.getCountOfDestinations()
        if (not session.get("index") is None):
            userData = userService.getUserSession(session.get("index"))
            if (userData[0]):
                name = userData[1].name
                firstname = name
                if " " in name:
                    firstname = name.split()[0]
            else:
                return render_template('home1.html', loggedIn=False, visits=totalVisits, plans=plans, noOfusers=noOfusers, places=places, warning="Login Required")
        else:
            return render_template('home1.html', loggedIn=False, visits=totalVisits, plans=plans, noOfusers=noOfusers, places=places, warning="Login Required")

        formdata = request.form
        startingDate = formdata.get('startingDate')
        endingDate = formdata.get('endingDate')
        state = formdata.get('state')
        if(startingDate > endingDate):
            return render_template("home1.html", firstname=firstname, loggedIn=True, type=userData[1].usertype, visits=totalVisits, plans=plans, noOfusers=noOfusers, places=places, warning="Invalid Dates")
        return redirect(url_for('plan.openingForm', state=state, startingDate=startingDate, endingDate=endingDate))


@app.route('/logo', methods=['GET'])
def logo():
    return send_file('static/assets/img/hero-img.png')


@app.route('/', methods=['GET'])
@app.route('/Home', methods=['GET'])
def redir():
    return redirect(url_for('home'))


@app.before_request
def beforeRequest():
    if(app.config["ENV"] == "production"):
        if not request.url.startswith('https'):
            return redirect(request.url.replace('http', 'https', 1))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
