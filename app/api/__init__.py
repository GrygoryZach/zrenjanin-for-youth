from flask import Blueprint

from .places import places_api_bp
from .events import events_api_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(places_api_bp)
api_bp.register_blueprint(events_api_bp)
