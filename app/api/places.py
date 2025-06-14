from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload
from sqlalchemy import exc, or_

from db import db_session
from models.__all_models import Place, PlaceCategory, Event  # Event is imported for the /places/<id>/events route

# Create a Blueprint specifically for Place-related APIs
places_api_bp = Blueprint('places_api', __name__, url_prefix='/api')


# GET a specific Place by ID
@places_api_bp.route('/places/<int:place_id>', methods=['GET'])
def get_place_by_id(place_id):
    db_sess = db_session.create_session()
    try:
        place = db_sess.query(Place).options(joinedload(Place.category)).get(place_id)
        if not place:
            return jsonify({"message": "Place not found."}), 404
        return jsonify(place.to_dict()), 200
    except Exception as e:
        return jsonify({"message": f"Error retrieving place: {str(e)}"}), 500
    finally:
        db_sess.close()


# GET Places: Find, filter, search, and paginate place data
@places_api_bp.route('/places', methods=['GET'])
def find_places():
    """
    Query string parameters:
        page (int, optional): The page number to retrieve. Default is 1.
        per_page (int, optional): The number of items per page. Default is 10.
        search (str, optional): A keyword to search for in place names or descriptions.
        categories (str, optional): A comma-separated string of categories names to filter by.

    Returns:
        JSON: A JSON object containing:
            - 'places' (list): A list of dictionaries, each representing a place.
            - 'total_places' (int): The total number of places matching the criteria (before pagination).
            - 'page' (int): The current page number.
            - 'per_page' (int): The number of items requested per page.
            - 'total_pages' (int): The total number of pages available.
        Status Code:
            200 OK: If places are successfully retrieved.
            500 Internal Server Error: If an unexpected error occurs during retrieval.
    """
    db_sess = db_session.create_session()
    try:
        query = db_sess.query(Place).options(joinedload(Place.category))

        # Apply categories filtering
        categories_param = request.args.get('categories')
        if categories_param:
            categories_list = [c.strip() for c in categories_param.split(',')]
            # Join with PlaceCategory table and filter by category name
            query = query.join(Place.category).filter(PlaceCategory.name.in_(categories_list))

        # Apply search filtering by name or description
        search_query = request.args.get('search')
        if search_query:
            search_pattern = f"%{search_query.lower()}%"
            # Use ilike for case-insensitive search
            query = query.filter(
                or_(
                    Place.name.ilike(search_pattern),
                    Place.description.ilike(search_pattern)
                )
            )

        # Pagination
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        total_places = query.count()
        places = query.offset((page - 1) * per_page).limit(per_page).all()
        places_dicts = [place.to_dict() for place in places]

        total_pages = (total_places + per_page - 1) // per_page

        return jsonify({
            "places": places_dicts,
            "total_places": total_places,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        }), 200

    except Exception as e:
        # Log the error for debugging purposes (consider using Flask's current_app.logger)
        print(f"Error in get_all_places: {e}")
        return jsonify({"message": f"Error retrieving places: {str(e)}"}), 500
    finally:
        db_sess.close()


# POST (Create) a new Place
@places_api_bp.route('/places', methods=['POST'])
def create_place():
    db_sess = db_session.create_session()
    try:
        data = request.json
        if not all(k in data for k in ['name', 'category_id']):
            return jsonify({"message": "Missing required fields: 'name' and 'category_id'."}), 400

        new_place = Place(
            name=data['name'],
            description=data.get('description'),
            position=data.get('position'),
            address=data.get('address'),
            category_id=data['category_id']
        )
        db_sess.add(new_place)
        db_sess.commit()

        # After commit, to ensure category relationship is available for .to_dict()
        # and to include the new ID, it's safest to refetch or manually construct response.
        # Refetching ensures all relationships are loaded for the new object.
        place_response = db_sess.query(Place).options(joinedload(Place.category)).get(new_place.id)

        return jsonify(place_response.to_dict()), 201  # 201 Created
    except exc.IntegrityError:
        db_sess.rollback()
        return jsonify(
            {"message": "Integrity error: Check category_id (ID might not exist) or unique constraints."}), 400
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error creating place: {str(e)}"}), 500
    finally:
        db_sess.close()


# PUT (Update) an existing Place
@places_api_bp.route('/places/<int:place_id>', methods=['PUT'])
def update_place(place_id):
    db_sess = db_session.create_session()
    try:
        data = request.json
        # Eager load category for the embedded category in to_dict for the response
        place = db_sess.query(Place).options(joinedload(Place.category)).get(place_id)
        if not place:
            return jsonify({"message": "Place not found."}), 404

        place.name = data.get('name', place.name)
        place.description = data.get('description', place.description)
        place.position = data.get('position', place.position)
        place.category_id = data.get('category_id', place.category_id)  # Update category_id if provided

        db_sess.commit()
        return jsonify(place.to_dict()), 200
    except exc.IntegrityError:
        db_sess.rollback()
        return jsonify({"message": "Integrity error: Check category_id or unique constraints."}), 400
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error updating place: {str(e)}"}), 500
    finally:
        db_sess.close()


# DELETE a Place
@places_api_bp.route('/places/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    db_sess = db_session.create_session()
    try:
        place = db_sess.query(Place).get(place_id)
        if not place:
            return jsonify({"message": "Place not found."}), 404

        db_sess.delete(place)
        db_sess.commit()
        return jsonify({"message": f"Place {place_id} deleted successfully."}), 200
    except exc.IntegrityError:
        db_sess.rollback()
        # Occurs if events still reference this place_id
        return jsonify({"message": "Cannot delete place due to existing related events."
                                   " Delete related events first or configure cascading deletes in your database."}), 409  # Conflict
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error deleting place: {str(e)}"}), 500
    finally:
        db_sess.close()


# GET all Events for a specific Place
@places_api_bp.route('/places/<int:place_id>/events', methods=['GET'])
def get_events_for_place(place_id):
    db_sess = db_session.create_session()
    try:
        place = db_sess.query(Place).get(place_id)
        if not place:
            return jsonify({"message": "Place not found."}), 404

        # Load events for this specific place, eager load their categories for to_dict
        events = db_sess.query(Event).filter_by(place_id=place_id).options(
            joinedload(Event.category)
        ).all()

        return jsonify([event.to_dict() for event in events]), 200
    except Exception as e:
        return jsonify({"message": f"Error retrieving events for place {place_id}: {str(e)}"}), 500
    finally:
        db_sess.close()


# GET basic categories (where parent_id is null)
@places_api_bp.route('/place_categories/basic', methods=['GET'])
def get_basic_categories():
    db_sess = db_session.create_session()
    try:
        basic_categories = db_sess.query(PlaceCategory).filter(PlaceCategory.parent_id.is_(None)).all()
        return jsonify([category.to_dict() for category in basic_categories]), 200
    except Exception as e:
        return jsonify({"message": f"Error retrieving basic categories: {str(e)}"}), 500
    finally:
        db_sess.close()


# --- PlaceCategory API Endpoints ---

# GET all PlaceCategories
@places_api_bp.route('/place_categories', methods=['GET'])
def get_all_place_categories():
    db_sess = db_session.create_session()
    try:
        categories = db_sess.query(PlaceCategory).all()
        return jsonify([category.to_dict() for category in categories]), 200
    except Exception as e:
        return jsonify({"message": f"Error retrieving place categories: {str(e)}"}), 500
    finally:
        db_sess.close()


# GET a specific PlaceCategory by ID
@places_api_bp.route('/place_categories/<int:category_id>', methods=['GET'])
def get_place_category_by_id(category_id):
    db_sess = db_session.create_session()
    try:
        category = db_sess.query(PlaceCategory).get(category_id)
        if not category:
            return jsonify({"message": "Place category not found."}), 404
        return jsonify(category.to_dict()), 200
    except Exception as e:
        return jsonify({"message": f"Error retrieving place category: {str(e)}"}), 500
    finally:
        db_sess.close()


# POST (Create) a new PlaceCategory
@places_api_bp.route('/place_categories', methods=['POST'])
def create_place_category():
    db_sess = db_session.create_session()
    try:
        data = request.json
        if not 'name' in data:
            return jsonify({"message": "Missing required field: 'name'."}), 400

        new_category = PlaceCategory(
            name=data['name'],
            parent_id=data.get('parent_id')
        )
        db_sess.add(new_category)
        db_sess.commit()
        return jsonify(new_category.to_dict()), 201
    except exc.IntegrityError as e:
        db_sess.rollback()
        if "UNIQUE constraint failed: place_categories.name" in str(e):
            return jsonify({"message": "Category name already exists."}), 400
        return jsonify({"message": f"Integrity error: {str(e)}"}), 400
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error creating place category: {str(e)}"}), 500
    finally:
        db_sess.close()


# PUT (Update) an existing PlaceCategory
@places_api_bp.route('/place_categories/<int:category_id>', methods=['PUT'])
def update_place_category(category_id):
    db_sess = db_session.create_session()
    try:
        data = request.json
        category = db_sess.query(PlaceCategory).get(category_id)
        if not category:
            return jsonify({"message": "Place category not found."}), 404

        category.name = data.get('name', category.name)
        category.parent_id = data.get('parent_id', category.parent_id)

        db_sess.commit()
        return jsonify(category.to_dict()), 200
    except exc.IntegrityError as e:
        db_sess.rollback()
        if "UNIQUE constraint failed: place_categories.name" in str(e):
            return jsonify({"message": "Category name already exists."}), 400
        return jsonify({"message": f"Integrity error: {str(e)}"}), 400
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error updating place category: {str(e)}"}), 500
    finally:
        db_sess.close()


# DELETE a PlaceCategory
@places_api_bp.route('/place_categories/<int:category_id>', methods=['DELETE'])
def delete_place_category(category_id):
    db_sess = db_session.create_session()
    try:
        category = db_sess.query(PlaceCategory).get(category_id)
        if not category:
            return jsonify({"message": "Place category not found."}), 404

        db_sess.delete(category)
        db_sess.commit()
        return jsonify({"message": f"Place category {category_id} deleted successfully."}), 200
    except exc.IntegrityError:
        db_sess.rollback()
        return jsonify({"message": "Cannot delete category due to existing related places or sub-categories."
                                   " Reassign them first."}), 409
    except Exception as e:
        db_sess.rollback()
        return jsonify({"message": f"Error deleting place category: {str(e)}"}), 500
    finally:
        db_sess.close()
