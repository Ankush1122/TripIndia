import os

from flask import Flask, render_template, redirect, session, send_file, request
from flask.helpers import url_for
from User import UserServices
from flask_mail import Message, Mail
from User.UserController import user
from Hotel.HotelController import hotel
from TouristsDestination.TouristDestinationController import touristdestination
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)

if(os.environ.get('ENV') == "Production"):
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(hotel, url_prefix="/hotel")
app.register_blueprint(touristdestination, url_prefix="/touristdestination")


mail = Mail(app)


userService = UserServices.UserServices(app.config)


@app.route('/home', methods=['GET'])
def home():
    if(app.config["ENV"] == "production"):
        userService.addView()
    totalVisits = userService.getTotalVisits()
    plans = 0
    noOfusers = userService.getNumberOfUsers()
    places = 1
    if (not session.get("index") is None):
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]
            return render_template("home.html", firstname=firstname, loggedIn=True, type=userData[1].usertype, visits=totalVisits, plans=plans, noOfusers=noOfusers, places=places)

    return render_template('home.html', loggedIn=False, visits=totalVisits, plans=plans, noOfusers=noOfusers, places=places)


@app.route('/logo', methods=['GET'])
def logo():
    return send_file('static/assets/img/hero-img.png')


@app.route('/', methods=['GET'])
@app.route('/Home', methods=['GET'])
def redir():
    return redirect(url_for('home'))


@app.route('/verificationlink/<token>')
def verificationlink(token):
    url = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = url.loads(token, salt=app.config["SALT"], max_age=600)
        userService.activateUser(email, 1)
        return render_template("emailverified.html", mail=email)

    except SignatureExpired:
        return "<h1>Your Link Expired</h1>"


@app.route('/verifyemail/<userid>')
def verifyemail(userid):

    url = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    token = url.dumps(userid,
                      salt=app.config["SALT"])
    print(token)
    mes = Message("Email Verification", recipients=[userid])
    mes.html = render_template(
        'verficationMail.html', link=url_for('verificationlink', token=token, _external=True))
    mail.send(mes)
    return render_template('emailsent.html', mail=userid)


@app.route('/sendImages/<destination>')
def sendImages(destination):
    mes = Message("TripIndia Uploaded Images", recipients=[
                  app.config.get("ADMIN_ADDRESS")])

    with app.open_resource(app.config.get("IMAGE_UPLOADS") + destination + "0.jpg") as img0:
        mes.attach(destination + "0.jpg", 'image/jpg', img0.read())

    with app.open_resource(app.config.get("IMAGE_UPLOADS") + destination + "1.jpg") as img1:
        mes.attach(destination + "1.jpg", 'image/jpg', img1.read())

    with app.open_resource(app.config.get("IMAGE_UPLOADS") + destination + "2.jpg") as img2:
        mes.attach(destination + "2.jpg", 'image/jpg', img2.read())

    with app.open_resource(app.config.get("IMAGE_UPLOADS") + destination + "3.jpg") as img3:
        mes.attach(destination + "3.jpg", 'image/jpg', img3.read())

    mail.send(mes)
    return redirect(url_for('touristdestination.exploreRajasthan'))


@app.before_request
def beforeRequest():
    if(app.config["ENV"] == "production"):
        if not request.url.startswith('https'):
            return redirect(request.url.replace('http', 'https', 1))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
