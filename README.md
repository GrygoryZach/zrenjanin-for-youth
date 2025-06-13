# 🏫 Zrenjanin for youth— School Edition

A web platform built for discovering interesting **places** and **events** in our local area.
Created as part of a school project, this application allows users to explore locations, filter by category, search by name or description, and view results on a map.

## 🌍 Features

* 🔎 **Search** for places and events by name or description
* 🗂 **Filter** by categories (e.g., parks, museums, concerts, etc.)
* 🗺 **Interactive map** (Leaflet + OpenStreetMap)
* 📅 **Events** are linked to real places, with position inherited from the location
* ⚡ Fully dynamic front-end (vanilla JS + fetch API)
* 🧠 Backend powered by Flask + SQLAlchemy

## 🚀 Technologies Used

* Python 3.x
* Flask
* SQLAlchemy
* Jinja2 (for templating)
* Leaflet.js (for map visualization)
* HTML5 + CSS3
* Vanilla JavaScript

## 📁 Project Structure

```
project/
├── app/                         # MAIN APPLICATION
│   ├── api/                     # api endpoints
│   │   ├── events.py
│   │   └── places.py
│   ├── config.py                # config
│   └── routes.py                # application routes
│
├── db/                          # DATABASE
│   ├── db_session.py            # database session management
│   └── zrenjanin.sqlite         # sqlite database file
│
├── models/                      # SQLALCHEMY MODELS
│
├── static/                      # STATIC FILES
│   ├── css/                     # css stylesheets
│   ├── js/                      # javascript files
│   └── uploads/                 # uploaded user files
│       ├── events/
│       └── places/
│
├── templates/                   # HTML TEMPLATES
│
├── tools/                       # TOOLS
│
├── requirements.txt             # project dependencies
└── run.py                       # application entry point
```

## 🔧 Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/GrygoryZach/zrenjanin-for-youth.git
   cd zrenjanin-for-youth
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the development server**

   ```bash
   python run.py
   ```

4. **Access the app**
   Navigate to `http://127.0.0.1:5000` in your browser.

## 🤝 Credits

Created by [Grisha](https://github.com/GrygoryZach) and classmates as a project for [Zrenjaninska Gimnazija](https://www.zrenjaninskagimnazija.edu.rs/).

---

To be continued ✌️
