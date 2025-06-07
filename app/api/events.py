from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload
from sqlalchemy import exc
from datetime import datetime

from db.db_session import create_session
from models.__all_models import Event, EventCategory, Place  # Place is imported for the /events/<id>/place route

# Create a Blueprint specifically for Event-related APIs
events_api_bp = Blueprint('events_api', __name__, url_prefix='/api')


# GET a specific Event by ID
@events_api_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    db_sess = create_session()
    try:
        # Eager load category for the embedded category in to_dict
        event = db_sess.query(Event).options(
            joinedload(Event.category)
        ).get(event_id)
        if not event:
            return jsonify({"message": "Event not found."}), 404
        return jsonify(event.to_dict()), 200
    except Exception as e:
        return jsonify({"message": f"Error retrieving event: {str(e)}"}), 500
    finally:
        db_sess.close()


# POST (Create) a new Event
@events_api_bp.route('/events', methods=['POST'])
def create_event():
    db_sess = create_session()
    try:
        data = request.json
        if not all(k in data for k in ['name', 'datetime', 'place_id', 'category_id']):
            return jsonify(
                {"message": "Missing required fields for event creation (name, datetime, place_id, category_id)."}), 400

        try:
            event_datetime = datetime.fromisoformat(data['datetime'])
        except ValueError:
            return jsonify({"message": "Invalid datetime format. Use ISO 8601 (e.g., 'YYYY-MM-DD HH:MM:SS')."}), 400

        new_event = Event(
            name=data['name'],
            description=data.get('description'),
            datetime=event_datetime,
            place_id=data['place_id'],
            category_id=data['category_id']
        )
        db_sess.add(new_event)
        db_sess.commit()

        # After commit, to ensure category relationship is available for .to_dict()
        event_response = db_sess.query(Event).options(
            joinedload(Event.category)
        ).get(new_event.id)

        return jsonify(event_response.to_dict()), 201
    except exc.IntegrityError:
        db_sess.rollback()
        return jsonify({"message": "Integrity error: Check place_id or category_id (IDs might not exist)."}), 400
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error creating event: {str(e)}"}), 500
    finally:
        db_sess.close()


# PUT (Update) an existing Event
@events_api_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    db_sess = create_session()
    try:
        data = request.json
        # Eager load category for the embedded category in to_dict for the response
        event = db_sess.query(Event).options(
            joinedload(Event.category)
        ).get(event_id)
        if not event:
            return jsonify({"message": "Event not found."}), 404

        event.name = data.get('name', event.name)
        event.description = data.get('description', event.description)
        event.place_id = data.get('place_id', event.place_id)
        event.category_id = data.get('category_id', event.category_id)

        if 'datetime' in data:
            try:
                event.datetime = datetime.fromisoformat(data['datetime'])
            except ValueError:
                return jsonify({"message": "Invalid datetime format. Use ISO 8601 (e.g., 'YYYY-MM-DD HH:MM:SS')."}), 400

        db_sess.commit()
        return jsonify(event.to_dict()), 200
    except exc.IntegrityError:
        db_sess.rollback()
        return jsonify({"message": "Integrity error: Check place_id or category_id."}), 400
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error updating event: {str(e)}"}), 500
    finally:
        db_sess.close()


# DELETE an Event
@events_api_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    db_sess = create_session()
    try:
        event = db_sess.query(Event).get(event_id)
        if not event:
            return jsonify({"message": "Event not found."}), 404

        db_sess.delete(event)
        db_sess.commit()
        return jsonify({"message": f"Event {event_id} deleted successfully."}), 200
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error deleting event: {str(e)}"}), 500
    finally:
        db_sess.close()


# GET the Place for a specific Event
@events_api_bp.route('/events/<int:event_id>/place', methods=['GET'])
def get_place_for_event(event_id):
    db_sess = create_session()
    try:
        # Eager load place AND its category for the place's to_dict
        event = db_sess.query(Event).options(
            joinedload(Event.place).joinedload(Place.category)  # Chain joinedload to get place's category
        ).get(event_id)
        if not event:
            return jsonify({"message": "Event not found."}), 404
        if not event.place:  # Should not happen if place_id is non-nullable, but good for robustness
            return jsonify({"message": "Place associated with this event not found."}), 404

        return jsonify(event.place.to_dict()), 200
    except Exception as e:
        return jsonify({"message": f"Error retrieving place for event {event_id}: {str(e)}"}), 500
    finally:
        db_sess.close()


# --- EventCategory API Endpoints ---

# GET a specific EventCategory by ID
@events_api_bp.route('/event_categories/<int:category_id>', methods=['GET'])
def get_event_category_by_id(category_id):
    db_sess = create_session()
    try:
        category = db_sess.query(EventCategory).get(category_id)
        if not category:
            return jsonify({"message": "Event category not found."}), 404
        return jsonify(category.to_dict()), 200
    except Exception as e:
        return jsonify({"message": f"Error retrieving event category: {str(e)}"}), 500
    finally:
        db_sess.close()


# POST (Create) a new EventCategory
@events_api_bp.route('/event_categories', methods=['POST'])
def create_event_category():
    db_sess = create_session()
    try:
        data = request.json
        if not 'name' in data:
            return jsonify({"message": "Missing required field: 'name'."}), 400

        new_category = EventCategory(
            name=data['name'],
            parent_id=data.get('parent_id')
        )
        db_sess.add(new_category)
        db_sess.commit()
        return jsonify(new_category.to_dict()), 201
    except exc.IntegrityError as e:
        db_sess.rollback()
        if "UNIQUE constraint failed: event_categories.name" in str(e):
            return jsonify({"message": "Category name already exists."}), 400
        return jsonify({"message": f"Integrity error: {str(e)}"}), 400
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error creating event category: {str(e)}"}), 500
    finally:
        db_sess.close()


# PUT (Update) an existing EventCategory
@events_api_bp.route('/event_categories/<int:category_id>', methods=['PUT'])
def update_event_category(category_id):
    db_sess = create_session()
    try:
        data = request.json
        category = db_sess.query(EventCategory).get(category_id)
        if not category:
            return jsonify({"message": "Event category not found."}), 404

        category.name = data.get('name', category.name)
        category.parent_id = data.get('parent_id', category.parent_id)

        db_sess.commit()
        return jsonify(category.to_dict()), 200
    except exc.IntegrityError as e:
        db_sess.rollback()
        if "UNIQUE constraint failed: event_categories.name" in str(e):
            return jsonify({"message": "Category name already exists."}), 400
        return jsonify({"message": f"Integrity error: {str(e)}"}), 400
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error updating event category: {str(e)}"}), 500
    finally:
        db_sess.close()


# DELETE an EventCategory
@events_api_bp.route('/event_categories/<int:category_id>', methods=['DELETE'])
def delete_event_category(category_id):
    db_sess = create_session()
    try:
        category = db_sess.query(EventCategory).get(category_id)
        if not category:
            return jsonify({"message": "Event category not found."}), 404

        db_sess.delete(category)
        db_sess.commit()
        return jsonify({"message": f"Event category {category_id} deleted successfully."}), 200
    except exc.IntegrityError:
        db_sess.rollback()
        return jsonify({"message": "Cannot delete category due to existing related events or sub-categories."
                                   " Reassign them first."}), 409
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error deleting event category: {str(e)}"}), 500
    finally:
        db_sess.close()
