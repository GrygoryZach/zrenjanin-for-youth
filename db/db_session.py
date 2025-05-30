from sqlalchemy import create_engine
import sqlalchemy.orm as orm
from os.path import exists

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Database file isn't specified!")

    db_exists = exists(db_file.strip())
    connection_string = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Connecting to the database at {connection_string}")

    engine = create_engine(connection_string, echo=False)
    __factory = orm.sessionmaker(bind=engine)


    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    global __factory
    return __factory()
