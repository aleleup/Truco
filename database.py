# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
db_username = os.getenv('DATABASE_USER_NAME')
db_pw = os.getenv('DATABASE_PASSWORD')



# 1. Cadena de conexión a la base de datos
# Asegúrate de reemplazar 'tu_usuario' y 'tu_contraseña'
# con tus credenciales de PostgreSQL.
DATABASE_URL = f"postgresql://{db_username}:{db_pw}@localhost:5432/TrucoDB"
print("URL: ", DATABASE_URL)
# 2. Crea el motor de la base de datos
# El 'engine' es el punto central para interactuar con la DB
# que gestiona la conexión subyacente.
engine = create_engine(DATABASE_URL)

# 3. Crea una "sesión" de la base de datos
# 'sessionmaker' es una fábrica de sesiones. Una sesión es
# como un área de trabajo donde realizas cambios en los objetos
# y luego los guardas en la base de datos con un 'commit'.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)