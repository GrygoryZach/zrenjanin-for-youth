from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('places', __name__)

# Full place data with coordinates and images (used in JS map and display)
places = [
    {
        "id": 1,
        "name": "Vinyl Bassic",
        "category": "entertainment",
        "latitude": 45.37995,
        "longitude": 20.39280,
        "image_url": "https://media.ilovezrenjanin.com/2024/05/vinyl-bassic-2-e1716305224556.jpg",
        "short_description": "Popularno mesto u centru grada sa muzičkim događajima i opuštenom atmosferom."
    },
    {
        "id": 2,
        "name": "Caffe Bridge",
        "category": "entertainment",
        "latitude": 45.37934,
        "longitude": 20.38927,
        "image_url": "https://scontent.fbeg7-2.fna.fbcdn.net/v/t39.30808-6/471450851_1144297101034417_3375446139899935729_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=833d8c&_nc_ohc=cqp7u19PUJkQ7kNvwFP4bxO&_nc_oc=AdmHaLa4vSYKPxpGesmmiXni7droYJuJYl4LsIkABoqvKOUB1-ae-O7I2KPc_gLDxNY&_nc_zt=23&_nc_ht=scontent.fbeg7-2.fna&_nc_gid=x9yGxgEB7FE_WkgSNTSXZw&oh=00_AfKAUpelC3FGSpVoqHQX-Bp8X8_86XE0xNPm_pf4m4y26A&oe=68290B22",
        "short_description": "Kafić sa prelepim pogledom na reku, idealan za opuštanje uz koktel ili kafu."
    },
    {
        "id": 3,
        "name": "Kulturni centar Zrenjanin",
        "category": "culture",
        "latitude": 45.37826,
        "longitude": 20.38999,
        "image_url": "https://105.rs/wp-content/uploads/2023/05/kulturni-centar-zr.png",
        "short_description": "Savremeni prostor za kulturna dešavanja u srcu grada, sa bogatim programom koncerata, izložbi i predstava."
    }
]

# Renders the main page and passes places to the template
@bp.route('/')
def index():
    return render_template("index.html", places=places)

# Optional: API route if you want to support search/category filters via fetch()
@bp.route('/api/places')
def api_places():
    category = request.args.get('category', '').lower()
    search = request.args.get('search', '').lower()

    filtered = places

    if category and category != "all":
        filtered = [p for p in filtered if p['category'].lower() == category]

    if search:
        filtered = [
            p for p in filtered
            if search in p['name'].lower() or search in p['short_description'].lower()
        ]

    return jsonify(filtered)
