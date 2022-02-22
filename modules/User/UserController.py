from flask import Blueprint, render_template, redirect, request, session, current_app, Flask
from flask.helpers import url_for
from User import UserModel, UserServices

from datetime import datetime

user = Blueprint("user", __name__, static_folder="static",
                 template_folder="templates")


@user.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("index") is not None:
        return redirect(url_for('home'))

    if (request.method == "POST"):

        form_data = request.form
        user = UserModel.User(None, None, form_data.get(
            "userid"), form_data.get("password"), None, None, None, None, None, None, None)

        now = datetime.now()
        currenttime = now.strftime("%d/%m/%Y %H:%M:%S")
        userService = UserServices.UserServices(current_app.config)
        dataRequest = userService.login(user)

        if (dataRequest[0]):
            if(dataRequest[1].verification == 0):
                return redirect(url_for('verifyemail', userid=dataRequest[1].userid))
            else:
                print("logged in successfully")
                session["index"] = dataRequest[1].index
                userService.addUserLog(user.userid, currenttime, 1)
                return redirect(url_for('home'))

        else:
            print("login failed")
            userService.addUserLog(user.userid, currenttime, 0)
            return render_template('login.html', warning=dataRequest[1])

    if (request.method == "GET"):
        return render_template('login.html')


@user.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if (not session.get("index") is None):
        userService = UserServices.UserServices(current_app.config)
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name

    else:
        return redirect(url_for('user.login'))

    if (request.method == "POST"):

        form_data = request.form

        user = UserModel.User(userData[1].index, form_data.get("name"), userData[1].userid, form_data.get(
            "password"), userData[1].usertype, userData[1].avatar, form_data.get("bio"), form_data.get("country"), form_data.get("occupation"), form_data.get("DOB"), userData[1].verification)
        userService = UserServices.UserServices(current_app.config)
        status = userService.editProfile(user)
        print(status[1])
        if(status[0]):
            return redirect(url_for('user.profile'))
        else:
            return render_template('editprofile.html', firstname=firstname, name=user.name, userid=user.userid, usertype=user.usertype, bio=user.bio, DOB=user.DOB, avatar=user.avatar, country=user.country, occupation=user.occupation, warning=status[1])

    if (request.method == "GET"):
        if " " in name:
            firstname = name.split()[0]
            return render_template('editprofile.html', firstname=firstname, name=name, userid=userData[1].userid, usertype=userData[1].usertype, bio=userData[1].bio, DOB=userData[1].DOB, avatar=userData[1].avatar, country=userData[1].country, occupation=userData[1].occupation)


@user.route('/profile', methods=['GET'])
def profile():
    if (not session.get("index") is None):
        userService = UserServices.UserServices(current_app.config)
        userData = userService.getUserSession(session.get("index"))
        name = userData[1].name
        firstname = name

        if " " in name:
            firstname = name.split()[0]

        if (userData[0]):
            return render_template('profile.html', firstname=firstname, name=name, userid=userData[1].userid, usertype=userData[1].usertype, bio=userData[1].bio, DOB=userData[1].DOB, avatar=userData[1].avatar, country=userData[1].country, occupation=userData[1].occupation)
        else:
            return redirect(url_for('user.login'))

    return redirect(url_for('user.login'))


@user.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    if (not session.get("index") is None):
        userService = UserServices.UserServices(current_app.config)
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]

    else:
        return redirect(url_for('user.login'))

    if (request.method == "POST"):

        form_data = request.form
        currentpassword = form_data["currentpassword"]
        newpassword = form_data["newpassword"]
        confirmpassword = form_data["confirmpassword"]

        userService = UserServices.UserServices(current_app.config)
        status = userService.changePassword(
            currentpassword, newpassword, confirmpassword, userData[1].userid)
        print(status[1])
        if(status[0]):
            return render_template('changepassword.html', firstname=firstname, name=userData[1].name, bio=userData[1].bio, avatar=userData[1].avatar, message=status[1])
        else:
            return render_template('changepassword.html', firstname=firstname, name=userData[1].name, bio=userData[1].bio, avatar=userData[1].avatar, warning=status[1])

    if (request.method == "GET"):

        if (userData[0]):
            return render_template('changepassword.html', firstname=firstname, name=name, bio=userData[1].bio, avatar=userData[1].avatar)
        else:
            return redirect(url_for('user.login'))


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    if (not session.get("index") is None):
        return redirect(url_for('home'))
    if(request.method == "POST"):
        form_data = request.form
        userService = UserServices.UserServices(current_app.config)
        status = userService.validateData(form_data.get("name"), form_data.get("email"), form_data.get(
            "password"), form_data.get("confirmpassword"), form_data.get("DOB"), form_data.get("DOB"))
        if(not status[0]):
            return render_template("signup.html", warning=status[1])
        user = UserModel.User(None, form_data.get("name"), form_data.get("email"), form_data.get(
            "password"), "user", 1, "Add Bio", form_data.get("country"), "Add Occupation", form_data.get("DOB"), 0)
        status = userService.register(user)
        if(not status[0]):
            return render_template("signup.html", warning=status[1])
        return redirect(url_for('verifyemail', userid=user.userid))
    if(request.method == "GET"):
        return render_template("signup.html")
    return redirect(url_for('sendmail', userid="deshmukh.1@iitj.ac.in"))


@user.route('/signout', methods=['GET'])
def signout():
    userService = UserServices.UserServices(current_app.config)
    userService.signout()
    return redirect(url_for('home'))


@user.route('/', methods=['GET'])
def redir():
    return redirect(url_for('user.login'))
