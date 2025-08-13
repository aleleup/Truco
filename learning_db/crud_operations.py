# crud_operations.py
from database import SessionLocal
from learning_db.models import User

# Obtener una sesión de la base de datos
db = SessionLocal()
user1 = User(name="Alice", email="alice@example.com")
user2 = User(name="Bob", email="bob@example.com")

def create_users():
    print("Creando nuevos usuarios...")
    db.add(user1)
    db.add(user2)
    db.commit() # Guarda los cambios en la base de datos
    db.refresh(user1) # Refresca el objeto para obtener el ID asignado
    db.refresh(user2)
    print(f"Usuarios creados: {user1.id} y {user2.id}")

def filter_users():
    # --- R (READ) - Leer y filtrar elementos ---
    print("\nLeyendo todos los usuarios:")
    all_users = db.query(User).all()
    for user in all_users:
        print(f"ID: {user.id}, Nombre: {user.name}")

    print("\nFiltrando por ID (leyendo un solo usuario):")
    alice = db.query(User).filter(User.id == user1.id).first()
    if alice:
        print(f"Encontrado: {alice.name}")

    print("\nFiltrando por email:")
    user_with_email = db.query(User).filter(User.email == "bob@example.com").first()
    if user_with_email:
        print(f"Encontrado: {user_with_email.name}")


def update_items():
    alice = db.query(User).filter(User.id == user1.id).first()

# --- U (UPDATE) - Actualizar un elemento ---
    print("\nActualizando el nombre de Alice...")
    if alice:
        alice.name = "Alicia"
        db.commit()
        db.refresh(alice) # Refresca el objeto para ver los cambios
        print(f"Nombre actualizado a: {alice.name}")

def delete_item(): 
    user_with_email = db.query(User).filter(User.email == "bob@example.com").first()
   
# --- D (DELETE) - Borrar un elemento ---
    print("\nBorrando el usuario Bob...")
    if user_with_email:
        db.delete(user_with_email)
        db.commit()
        print("Usuario Bob borrado con éxito.")

# --- Borrar toda la tabla (Precaución) ---
# Si quisieras borrar todos los registros de la tabla, harías algo así:
# db.query(User).delete()
# db.commit()



# --- Borrar la tabla completa de la base de datos ---
# Esto es muy destructivo. Solo úsalo si quieres eliminar la estructura de la tabla
# de la base de datos.
# from database import Base, engine
# Base.metadata.drop_all(bind=engine)

# Cerrar la sesión
db.close()