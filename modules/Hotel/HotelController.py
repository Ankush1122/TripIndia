from flask import Blueprint, render_template, redirect, request, current_app
from flask.helpers import url_for


hotel = Blueprint("hotel", __name__, static_folder="static",
                  template_folder="templates")


@hotel.route('/explore/states', methods=['GET'])
def state():
    return render_template("state.html")


@hotel.route('/explore/works', methods=['GET'])
def works():
    return render_template("works.html")


@hotel.route('/', methods=['GET'])
def redir():
    return redirect(url_for('hotel.explore'))
