# create_tables.py
from database import engine
from learning_db.models import User, Base



def create_first_table() -> None:

    print("Creando tablas en la base de datos...")
    # Este comando crea todas las tablas definidas en Base.metadata
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas con éxito!")

