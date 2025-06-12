from flask import Blueprint, render_template
from db import db_session
from models.__all_models import Place

bp = Blueprint('routes', __name__)


@bp.route('/')
def main_page():
    return render_template("main_page.html")


@bp.route('/about')
def about():
    return render_template("about.html")


@bp.route('/place_search')
def place_search():
    return render_template("place_search.html")


@bp.route('/places/<int:place_id>')
def place_details(place_id: int):
    db_sess = db_session.create_session()
    place = db_sess.query(Place).get(place_id)
    place_dict = place.to_dict()
    return render_template("place_details.html", place=place_dict)

