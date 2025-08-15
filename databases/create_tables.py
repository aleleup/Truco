# create_tables.py
from database import engine
from databases.tables_schemas import *



def create_tables() -> None:
    try:
        print("Starting table creation process")
        Base.metadata.create_all(bind=engine)
        print("Tables created succesfully")
    except Exception as e:
        print(f"Error at table creation: \n {e}")
