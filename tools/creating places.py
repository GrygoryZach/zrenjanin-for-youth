import requests
import json
import time
import re  # Uvozimo modul za regularne izraze

# --- Konfiguracija API-ja ---
YOUR_API_BASE_URL = "http://127.0.0.1:5000/api"  # Baza URL vašeg API-ja
YOUR_API_CREATE_PLACE_URL = f"{YOUR_API_BASE_URL}/places"
YOUR_API_CATEGORIES_URL = f"{YOUR_API_BASE_URL}/place_categories"

# --- Mapa OSM tagova na vaše kategorije ---
OSM_CATEGORY_MAP = {
    # Hrana i piće
    'restaurant': 'Hrana i piće',
    'cafe': 'Hrana i piće',
    'fast_food': 'Hrana i piće',
    'bar': 'Hrana i piće',
    'pub': 'Hrana i piće',
    'bakery': 'Hrana i piće',
    'confectionery': 'Hrana i piće',
    'ice_cream': 'Hrana i piće',

    # Kultura i umetnost
    'museum': 'Kultura i umetnost',
    'theatre': 'Kultura i umetnost',
    'arts_centre': 'Kultura i umetnost',
    'gallery': 'Kultura i umetnost',
    'library': 'Kultura i umetnost',
    'cinema': 'Kultura i umetnost',
    'memorial': 'Kultura i umetnost',
    'monument': 'Kultura i umetnost',
    'historic': 'Kultura i umetnost',
    'art': 'Kultura i umetnost',  # Generalniji tag

    # Sport i rekreacija
    'sports_centre': 'Sport i rekreacija',
    'stadium': 'Sport i rekreacija',
    'pitch': 'Sport i rekreacija',
    'playground': 'Sport i rekreacija',
    'gym': 'Sport i rekreacija',
    'fitness_centre': 'Sport i rekreacija',
    'swimming_pool': 'Sport i rekreacija',
    'sports': 'Sport i rekreacija',  # Generalniji tag

    # Parkovi i priroda
    'park': 'Parkovi i priroda',
    'garden': 'Parkovi i priroda',
    'nature_reserve': 'Parkovi i priroda',
    'river': 'Parkovi i priroda',
    'water': 'Parkovi i priroda',
    'lake': 'Parkovi i priroda',
    'natural': 'Parkovi i priroda',  # Generalniji tag

    # Edukacija
    'school': 'Edukacija',
    'university': 'Edukacija',
    'college': 'Edukacija',
    'kindergarten': 'Edukacija',
    'language_school': 'Edukacija',
    'education': 'Edukacija',  # Generalniji tag

    # Kupovina
    'supermarket': 'Kupovina',
    'mall': 'Kupovina',
    'clothes': 'Kupovina',
    'boutique': 'Kupovina',
    'shopping_centre': 'Kupovina',
    'shop': 'Kupovina',  # opšta kategorija za prodavnice
    'retail': 'Kupovina',  # Generalniji tag

    # Izlazak i druženje
    'nightclub': 'Izlazak i druženje',
    'community_centre': 'Izlazak i druženje',
    'social_facility': 'Izlazak i druženje',
    'event_venue': 'Izlazak i druženje',  # Mesta za događaje
    'leisure': 'Izlazak i druženje',  # Opšta kategorija za zabavu
    'place_of_worship': 'Izlazak i druženje',  # Ako se koriste za okupljanje
    'library': 'Izlazak i druženje',  # Biblioteka može biti i za druženje/rad

    # Podrazumevana kategorija ako se ništa ne poklapa
    'default_category': 'Ostalo ',  # Sa razmakom na kraju, kao što je u vašoj bazi
}

# Keš za ID-jeve kategorija - popunjava se pozivom API-ja
category_name_to_id_map = {}


# --- Funkcija za dohvat ID-jeva kategorija iz vašeg API-ja ---
def fetch_categories_from_api(api_url: str) -> dict:
    """
    Dohvata listu kategorija iz vašeg API-ja i kreira mapu
    naziv_kategorije -> category_id.
    """
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        categories = response.json()

        category_map = {}
        for cat in categories:
            clean_name = cat['name'].strip()  # Uklanja razmake sa krajeva
            latin_name = to_serbian_latin(clean_name)
            category_map[latin_name] = cat['id']
            category_map[clean_name] = cat['id']  # Dodato radi sigurnosti, ako je već latinica
        return category_map
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Greška pri dohvatanju kategorija sa API-ja '{api_url}': {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"  ❌ Greška parsiranja JSON-a od API-ja za kategorije: {e}")
        return {}
    except Exception as e:
        print(f"  ❌ Nepredviđena greška pri dohvatanju kategorija: {e}")
        return {}


# --- Funkcija za transliteraciju ćirilice u latinicu ---
def to_serbian_latin(text: str) -> str:
    """
    Prebacuje srpsku ćirilicu u srpsku latinicu.
    """
    if not isinstance(text, str):
        return text

    cyrillic_to_latin_map = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Ђ': 'Đ', 'Е': 'E', 'Ж': 'Ž', 'З': 'Z', 'И': 'I',
        'Ј': 'J', 'К': 'K', 'Л': 'L', 'Љ': 'Lj', 'М': 'M', 'Н': 'N', 'Њ': 'Nj', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'Ћ': 'Ć', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C', 'Ч': 'Č', 'Џ': 'Dž', 'Ш': 'Š',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ђ': 'đ', 'е': 'e', 'ж': 'ž', 'з': 'z', 'и': 'i',
        'ј': 'j', 'к': 'k', 'л': 'l', 'љ': 'lj', 'м': 'm', 'н': 'n', 'њ': 'nj', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'ћ': 'ć', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'č', 'џ': 'dž', 'ш': 'š'
    }

    latin_text = []
    i = 0
    while i < len(text):
        char = text[i]

        # Provera za 'Nj', 'Lj', 'Dž' kao celinu
        if i + 1 < len(text):
            two_chars = text[i:i + 2]
            if two_chars == 'Њ' or two_chars == 'њ':
                latin_text.append('Nj' if char == 'Њ' else 'nj')
                i += 1  # Povećava se za 1, jer smo već obradili dva znaka kao jedan digraf
            elif two_chars == 'Љ' or two_chars == 'љ':
                latin_text.append('Lj' if char == 'Љ' else 'lj')
                i += 1
            elif two_chars == 'Џ' or two_chars == 'џ':
                latin_text.append('Dž' if char == 'Џ' else 'dž')
                i += 1
            else:
                latin_text.append(cyrillic_to_latin_map.get(char, char))
        else:  # Samo jedan karakter preostao
            latin_text.append(cyrillic_to_latin_map.get(char, char))
        i += 1

    return ''.join(latin_text)


# --- Interakcija sa OpenStreetMap API-jem ---
def get_place_details_from_osm_raw(place_name: str, city: str = "Zrenjanin", limit: int = 1) -> list:
    base_url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "my-place-app-pure-requests"
    }

    params = {
        "q": f"{place_name}, {city}",
        "format": "json",
        "limit": limit,
        "addressdetails": 1,
        "extratags": 1,
        "namedetails": 1
    }

    request_url = requests.Request('GET', base_url, params=params).prepare().url
    print(f"Zahtev ka OSM: {request_url}")

    places_data = []  # Lista za čuvanje više mesta

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            print(f"  ❌ Greška OSM: Mesto '{place_name}' nije pronađeno u '{city}'. Pokušajte da precizirate pretragu.")
            return []

        for osm_result in data:  # Preimenovano iz 'first_result' u 'osm_result' radi jasnoće
            clean_name = place_name
            if "address" in osm_result and "name" in osm_result["address"]:
                clean_name = osm_result["address"]["name"]
            elif "extratags" in osm_result and isinstance(osm_result["extratags"], dict) and "name" in \
                    osm_result["extratags"]:
                clean_name = osm_result["extratags"]["name"]
            elif "osm_type" in osm_result and osm_result["osm_type"] == "node" and isinstance(osm_result.get("tags"),
                                                                                              dict) and "name" in \
                    osm_result["tags"]:
                clean_name = osm_result["tags"]["name"]
            else:
                parts = osm_result.get("display_name", "").split(',')
                if parts and parts[0].strip() != city:
                    clean_name = parts[0].strip()

            lat = osm_result.get("lat")
            lon = osm_result.get("lon")

            address_string_parts = []
            if "address" in osm_result:
                address_data = osm_result["address"]

                street_info = []
                if "road" in address_data:
                    street_info.append(address_data["road"])
                if "house_number" in address_data:
                    street_info.append(address_data["house_number"])

                if street_info:
                    address_string_parts.append(" ".join(street_info))

                district = None
                if "suburb" in address_data:
                    district = address_data["suburb"]
                elif "city_district" in address_data:
                    district = address_data["city_district"]
                elif "village" in address_data and address_data["village"].lower() != city.lower():
                    district = address_data["village"]

                if district:
                    address_string_parts.append(district)

            address_string = ", ".join(address_string_parts) if address_string_parts else osm_result.get(
                "display_name", "")

            if not lat or not lon or not address_string_parts:
                print(
                    f"  ⚠️ Upozorenje OSM: Delimični podaci za '{clean_name}' (originalni upit: '{place_name}'). Proverite URL.")

            # --- ODREĐIVANJE KATEGORIJE NA OSNOVU OSM TAGOVA ---
            determined_category_name = OSM_CATEGORY_MAP['default_category']  # Podrazumevana vrednost

            tags_to_check = {}
            if isinstance(osm_result.get("extratags"), dict):
                tags_to_check.update(osm_result["extratags"])
            if isinstance(osm_result.get("tags"), dict):
                tags_to_check.update(osm_result["tags"])

            found_category = False
            for osm_key, osm_value in tags_to_check.items():
                if osm_value in OSM_CATEGORY_MAP:
                    determined_category_name = OSM_CATEGORY_MAP[osm_value]
                    found_category = True
                    break
                if osm_key in OSM_CATEGORY_MAP:
                    determined_category_name = OSM_CATEGORY_MAP[osm_key]
                    found_category = True
                    break

            if not found_category:
                osm_class = osm_result.get("class")
                osm_type = osm_result.get("type")

                if osm_class in OSM_CATEGORY_MAP:
                    determined_category_name = OSM_CATEGORY_MAP[osm_class]
                elif osm_type in OSM_CATEGORY_MAP:
                    determined_category_name = OSM_CATEGORY_MAP[osm_type]

            # --- Prevod u srpsku latinicu i dohvat ID-a kategorije ---
            final_name = to_serbian_latin(clean_name)
            final_address = to_serbian_latin(address_string)

            category_id_to_use = category_name_to_id_map.get(
                to_serbian_latin(determined_category_name).strip(),
                category_name_to_id_map.get(OSM_CATEGORY_MAP['default_category'].strip())
            )
            if category_id_to_use is None:
                print(
                    f"  ❌ Greška: ID za kategoriju '{determined_category_name.strip()}' ili podrazumevanu kategoriju 'Ostalo' nije pronađen u vašem API-ju. Preskačem mesto '{final_name}'.")
                continue  # Preskoči ovo mesto i pređi na sledeće

            places_data.append({
                'id': None,
                'name': final_name,
                'description': None,
                'position': f"{lat},{lon}" if lat and lon else None,
                'address': final_address,
                'category_id': category_id_to_use,
                'image_url': None
            })
        return places_data
    except requests.exceptions.HTTPError as e:
        print(
            f"  ❌ HTTP greška Nominatim: Status {e.response.status_code} za '{place_name}'. Odgovor: {e.response.text.strip()}")
        return []
    except requests.exceptions.ConnectionError as e:
        print(
            f"  ❌ Greška konekcije Nominatim: Nije moguće povezati se sa serverom za '{place_name}'. Proverite internet ili URL. {e}")
        return []
    except requests.exceptions.Timeout as e:
        print(f"  ❌ Greška isteka vremena Nominatim: Zahtev ka OSM za '{place_name}' je predugo trajao. {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Opšta greška zahteva Nominatim za '{place_name}': {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"  ❌ Greška parsiranja JSON-a od Nominatim-a za '{place_name}': Neispravan odgovor servera. {e}")
        return []
    except Exception as e:
        print(f"  ❌ Nepredviđena greška prilikom obrade OSM podataka za '{place_name}': {e}")
        return []


# --- Funkcija za slanje podataka API-ju ---
def submit_place_to_api(place_data: dict) -> bool:
    if not YOUR_API_CREATE_PLACE_URL:
        print("Greška: Nije naveden URL za vaš API. Postavite YOUR_API_CREATE_PLACE_URL.")
        return False

    data_to_send = place_data.copy()
    data_to_send.pop('id', None)
    data_to_send.pop('image_url', None)

    print(
        f"Pokušavam da pošaljem podatke u API: '{data_to_send.get('name')}' (kategorija ID: {data_to_send.get('category_id')})")

    try:
        response = requests.post(YOUR_API_CREATE_PLACE_URL, json=data_to_send)
        response.raise_for_status()

        print(f"Uspešno kreirano mesto '{place_data.get('name')}'. Odgovor API-ja: {response.json()}")
        return True
    except requests.exceptions.HTTPError as e:
        print(
            f"  ❌ HTTP greška API: Prilikom slanja '{place_data.get('name')}'. Status: {e.response.status_code}. Odgovor: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Greška zahteva API-ja prilikom slanja '{place_data.get('name')}': {e}")
    except Exception as e:
        print(f"  ❌ Nepredviđena greška prilikom slanja '{place_data.get('name')}': {e}")
    return False


def parse_user_input(user_input: str) -> list[tuple[str, int]]:
    """
    Parsira korisnički unos koji može biti pojedinačni string,
    ili JSON lista stringova, sa opcionalnim limitom rezultata u zagradama.
    Vraća listu torki (place_name, limit_val).
    """
    processed_items = []

    if user_input.lower() == 'stop':
        return []
    elif user_input.startswith('[') and user_input.endswith(']'):
        try:
            temp_list = json.loads(user_input.replace("'", '"'))
            if not isinstance(temp_list, list):
                print("Greška: Uneta lista nije validna Python lista. Molimo pokušajte ponovo.")
                return []
            for item in temp_list:
                if isinstance(item, str):
                    match = re.search(r'^(.*?)\s*\((\d+)\)$', item)
                    if match:
                        place_name = match.group(1).strip()
                        limit_val = int(match.group(2))
                        processed_items.append((place_name, limit_val))
                    else:
                        processed_items.append((item.strip(), 1))  # Podrazumevano 1 rezultat
                else:
                    print(f"Upozorenje: Element liste '{item}' nije validan string. Biće preskočen.")
        except json.JSONDecodeError:
            print("Greška: Uneti string nije validna JSON lista. Molimo pokušajte ponovo.")
    else:  # Jednostruki unos
        match = re.search(r'^(.*?)\s*\((\d+)\)$', user_input)
        if match:
            place_name = match.group(1).strip()
            limit_val = int(match.group(2))
            processed_items.append((place_name, limit_val))
        else:
            processed_items.append((user_input.strip(), 1))  # Podrazumevano 1 rezultat

    return processed_items


def process_and_submit_places(
        search_items: list[tuple[str, int]],
        city: str,
        all_places_data: list,
        all_submitted_places: list,
        all_queries: list
) -> None:
    """
    Procesira listu upita (naziv mesta, limit), dohvata podatke sa OSM-a
    i šalje ih na vaš API.
    """
    for item, limit_val in search_items:
        query_display = f"{item} ({limit_val})" if limit_val > 1 else item
        all_queries.append(query_display)

        places_from_osm = get_place_details_from_osm_raw(item, city=city, limit=limit_val)
        if places_from_osm:
            for place_data in places_from_osm:
                all_places_data.append(place_data)
                if submit_place_to_api(place_data):
                    all_submitted_places.append(place_data)
                time.sleep(0.5)  # Mali prekid između slanja svakog mesta


if __name__ == "__main__":
    print(f"Pokušavam da dohvatim kategorije sa vašeg API-ja: {YOUR_API_CATEGORIES_URL}")
    category_name_to_id_map = fetch_categories_from_api(YOUR_API_CATEGORIES_URL)

    if not category_name_to_id_map:
        print("Fatalna greška: Nije moguće dohvatiti kategorije sa API-ja. Proverite URL i da li je API aktivan.")
        exit()

    if OSM_CATEGORY_MAP['default_category'].strip() not in category_name_to_id_map:
        print(
            f"Upozorenje: Podrazumevana kategorija '{OSM_CATEGORY_MAP['default_category'].strip()}' nije pronađena u API-ju. ")
        print("Molimo dodajte je u vašu bazu podataka ili promenite 'default_category' u skripti.")

    all_places_data = []
    all_queries = []
    all_submitted_places = []

    fixed_city = "Zrenjanin"

    print(
        f"Unesite naziv mesta ili listu mesta u {fixed_city} (npr. 'kafe (3)', 'muzej', ['park (2)', 'biblioteka']) ili 'stop' za završetak: ")

    first_input = input().strip()

    # Procesirajte prvi unos
    parsed_first_input = parse_user_input(first_input)
    process_and_submit_places(parsed_first_input, fixed_city, all_places_data, all_submitted_places, all_queries)

    # Nastavite sa unosom dok korisnik ne unese 'stop'
    if not (first_input.lower() == 'stop' or (first_input.startswith('[') and first_input.endswith(']'))):
        while True:
            user_input = input(
                f"Unesite sledeći naziv mesta u {fixed_city} (npr. 'muzej (2)') ili 'stop' za završetak: ").strip()
            if user_input.lower() == 'stop':
                break

            parsed_input = parse_user_input(user_input)
            process_and_submit_places(parsed_input, fixed_city, all_places_data, all_submitted_places, all_queries)

    print("\n--- Svi prikupljeni podaci o mestima (iz OSM) ---")
    for place in all_places_data:
        print(place)

    print("\n--- Mesta uspešno poslata u API ---")
    for place in all_submitted_places:
        print(place)

    print("\n--- Svi korisnički upiti ---")
    for query in all_queries:
        print(query)
