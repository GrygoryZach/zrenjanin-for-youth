from flask import Flask, jsonify, request
import os
import glob
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

IMAGE_BASE_PATH = "/static/uploads/places"
DB_IMAGE_PREFIX = "static/uploads/places/"


# --- Funkcije za obradu slika i baze podataka (premeštene u rutu ili pozvane iz nje) ---

def get_image_files_sorted_by_creation_date(folder_path: str) -> list[str]:
    image_files = []
    allowed_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']

    print(f"Skeniram folder za slike: {folder_path}")
    for ext in allowed_extensions:
        for filepath in glob.glob(os.path.join(folder_path, ext)):
            try:
                modification_timestamp = os.path.getmtime(filepath)
                image_files.append((filepath, modification_timestamp))
            except OSError as e:
                print(f"  ⚠️ Upozorenje: Nije moguće dohvatiti informacije o fajlu '{filepath}': {e}")

    image_files.sort(key=lambda x: x[1], reverse=False)

    sorted_paths = [file_info[0] for file_info in image_files]
    print(f"Pronađeno i sortirano {len(sorted_paths)} slika.")
    return sorted_paths


def update_place_image_urls_in_db():
    db_sess = db_session.create_session()

    try:
        sorted_image_paths = get_image_files_sorted_by_creation_date(IMAGE_BASE_PATH)

        if not sorted_image_paths:
            return {"status": "error", "message": "Nema pronađenih slika u navedenom folderu."}, 404

        places = db_sess.query(Place).order_by(Place.id).all()

        if not places:
            return {"status": "error", "message": "Nema pronađenih mesta u bazi podataka."}, 404

        print(f"Pronađeno {len(places)} mesta u bazi podataka.")
        updated_count = 0

        for i, place in enumerate(places):
            if i < len(sorted_image_paths):
                full_image_path = sorted_image_paths[i]
                filename = os.path.basename(full_image_path)
                db_image_url = os.path.join(DB_IMAGE_PREFIX, filename).replace('\\', '/')

                if place.image_url != db_image_url:
                    place.image_url = db_image_url
                    updated_count += 1
                    print(f"  Ažuriram Mesto ID: {place.id}, Naziv: '{place.name}' sa URL-om: '{db_image_url}'")
                else:
                    print(f"  Mesto ID: {place.id}, Naziv: '{place.name}' već ima ispravan URL: '{db_image_url}'")
            else:
                print(
                    f"  ⚠️ Upozorenje: Nema više slika za dodelu. Mesto ID: {place.id}, Naziv: '{place.name}' neće biti ažurirano.")
                break

        db_sess.commit()
        return {"status": "success",
                "message": f"Uspešno ažurirano {updated_count} URL-ova slika u bazi podataka."}, 200

    except SQLAlchemyError as e:
        db_sess.rollback()
        return {"status": "error", "message": f"Greška baze podataka: {str(e)}"}, 500
    except Exception as e:
        db_sess.rollback()
        return {"status": "error", "message": f"Neočekivana greška: {str(e)}"}, 500
    finally:
        db_sess.close()


@bp.route('/add_places', methods=['GET'])
def add_places_route():
    """
    Ruta za ažuriranje URL-ova slika za mesta u bazi podataka.
    Očekuje POST zahtev.
    """
    print("Primljen zahtev za /add_places rutu.")
    response, status_code = update_place_image_urls_in_db()
    return jsonify(response), status_code
