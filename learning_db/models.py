from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Esta es la base para todas tus clases de modelos
Base = declarative_base()

class User(Base):
    """
    Clase que representa la tabla 'users' en la base de datos.
    """
    __tablename__ = "users"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)



class MyExample(Base):
    __tablename__ = "table_example"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, primary_key=False)