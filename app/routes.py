from flask import Blueprint, render_template

bp = Blueprint('routes', __name__)


@bp.route('/')
def index():
    places = [
        {
            "id": 1,
            "name": "Ultra Caffe",
            "category": "Zabava",
            "latitude": 45.3836,
            "longitude": 20.3883,
            "image_url": "https://www.tripadvisor.com/LocationPhotoDirectLink-g304108-d8483641-i222539700-UltraCaffe-Zrenjanin_Vojvodina.html",
            "short_description": "Popularno mesto u centru grada sa muzičkim događajima i opuštenom atmosferom."
        },
        {
            "id": 2,
            "name": "Caffe Bridge",
            "category": "Zabava",
            "latitude": 45.3848,
            "longitude": 20.3884,
            "image_url": "https://www.top-rated.online/cities/Zrenjanin/place/p/4598519/Bridge",
            "short_description": "Kafić sa prelepim pogledom na reku, idealan za opuštanje uz koktel ili kafu."
        },
        {
            "id": 3,
            "name": "Caffe Papagaj",
            "category": "Zabava",
            "latitude": 45.3832,
            "longitude": 20.3879,
            "image_url": "https://www.zrklik.com/2022/06/potrebna-devojka-za-rad-u-kaficu-papagaj-odlicni-uslovi/",
            "short_description": "Tradicija duga 26 godina, poznat po prijatnoj atmosferi i ljubavi prema dobroj kafi."
        }
    ]
    return render_template("index.html", places=places, page=1, has_next=True)
