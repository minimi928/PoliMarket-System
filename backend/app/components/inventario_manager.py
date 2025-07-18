from sqlalchemy.orm import Session
from ..models.entities import Inventario, Producto
from ..models.schemas import InventarioCreate, ProductoCreate

class InventarioManager:
    """Componente para gestión de inventario (RF03)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def verificar_disponibilidad(self, producto_id: int, cantidad: int) -> bool:
        """Verifica disponibilidad de un producto (RF03)"""
        inventario = self.db.query(Inventario).filter(Inventario.producto_id == producto_id).first()
        return inventario and inventario.cantidad_disponible >= cantidad
    
    def consultar_inventario(self, producto_id: int) -> Inventario:
        """Consulta inventario de un producto (RF03)"""
        return self.db.query(Inventario).filter(Inventario.producto_id == producto_id).first()
    
    def actualizar_stock(self, producto_id: int, cantidad: int) -> bool:
        """Actualiza el stock de un producto (RF03)"""
        try:
            inventario = self.db.query(Inventario).filter(Inventario.producto_id == producto_id).first()
            if not inventario:
                return False
            
            inventario.cantidad_disponible += cantidad
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error actualizando stock: {e}")
            return False
    
    def consultar_productos_bajo_stock(self):
        """Consulta productos con stock bajo (RF03)"""
        return self.db.query(Inventario).filter(
            Inventario.cantidad_disponible <= Inventario.cantidad_minima
        ).all()

class ProductoManager:
    """Componente para gestión de productos (RF03)"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def crear_producto(self, producto_data: ProductoCreate) -> Producto:
        """Crea un nuevo producto (RF03)"""
        try:
            producto = Producto(
                nombre=producto_data.nombre,
                descripcion=producto_data.descripcion,
                precio=producto_data.precio,
                categoria=producto_data.categoria,
                proveedor_id=producto_data.proveedor_id
            )
            self.db.add(producto)
            self.db.commit()
            self.db.refresh(producto)
            return producto
        except Exception as e:
            self.db.rollback()
            print(f"Error creando producto: {e}")
            return None
    
    def consultar_producto(self, producto_id: int) -> Producto:
        """Consulta un producto por ID (RF03)"""
        return self.db.query(Producto).filter(Producto.id == producto_id).first()
    
    def listar_productos(self):
        """Lista todos los productos (RF03)"""
        return self.db.query(Producto).all()
    
    def buscar_productos_por_categoria(self, categoria: str):
        """Busca productos por categoría (RF03)"""
        return self.db.query(Producto).filter(Producto.categoria == categoria).all() 