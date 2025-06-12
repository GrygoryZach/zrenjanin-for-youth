from flask import Blueprint, render_template

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
