from sqlalchemy import text
from app.models.database import SessionLocal, engine

def truncate_database():
    """Elimina todas las tablas y las recrea desde cero"""
    db = SessionLocal()
    
    try:
        # Desactivar restricciones de clave foránea temporalmente
        db.execute(text("PRAGMA foreign_keys=OFF"))
        
        # Obtener todas las tablas
        tables = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"))
        table_names = [table[0] for table in tables]
        
        print(f"Eliminando tablas: {table_names}")
        
        # Eliminar todas las tablas
        for table_name in table_names:
            db.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            print(f"Tabla {table_name} eliminada")
        
        db.commit()
        print("Todas las tablas han sido eliminadas")
        
    except Exception as e:
        db.rollback()
        print(f"Error eliminando tablas: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    truncate_database()
    print("Ejecuta 'python init_data.py' para recrear las tablas con datos de ejemplo") 