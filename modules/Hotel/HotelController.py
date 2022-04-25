from flask import Blueprint, render_template, redirect, request, current_app, session
from flask.helpers import url_for

hotel = Blueprint("hotel", __name__, static_folder="static",
                  template_folder="templates")


from User import UserServices
from Hotel import HotelModel
from Hotel import HotelServices
from app import db

userService = UserServices.UserServices(db)
hotelServices = HotelServices.Services(db)


@hotel.route('/addHotel', methods=['GET', 'POST'])
def addHotel():
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

    if(userType != "superadmin"):
        return "You Are Not Authorized To Access This Page"

    if(request.method == "POST"):
        form = request.form
        hotel = HotelModel.Model(form.get('name'), form.get('city'), int(form.get('hotelType')), int(form.get(
            'roomCapacity')), form.get('roomPrice'), form.get('longitude'), form.get('latitude'))
        data = hotelServices.addHotel(hotel)
        if(data[0]):
            return render_template("addHotel.html", firstname=firstname, type=userType, success=data[1])
        else:
            return render_template("addHotel.html", firstname=firstname, type=userType, warning=data[1])

    elif(request.method == "GET"):
        return render_template("addHotel.html", firstname=firstname, type=userType)
