from app import create_app
from db import db_session
from models.__all_models import *

app = create_app()

if __name__ == "__main__":
    db_session.global_init("db/zrenjanin.sqlite")
    app.run(debug=True)
